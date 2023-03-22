import sys
import datacube
import numpy as np
import xarray as xr
from deafrica_tools.datahandling import load_ard
from deafrica_tools.bandindices import calculate_indices
from odc.algo import xr_geomedian
from datacube.utils import masking


def geomedian_with_indices_wrapper(ds):
    """Apply xr_geomedian function and calculate a series of indices"""

    indices = ["NDVI", "LAI", "SAVI", "MSAVI", "MNDWI"]
    satellite_mission = "s2"

    ds_geomedian = xr_geomedian(ds)

    ds_geomedian = calculate_indices(
        ds_geomedian,
        index=indices,
        drop=False,
        satellite_mission=satellite_mission,
    )

    return ds_geomedian


def indices_wrapper(ds):
    """Calculate list of indices"""

    indices = ["NDVI", "LAI", "SAVI", "MSAVI", "MNDWI"]
    satellite_mission = "s2"

    ds = calculate_indices(
        ds,
        index=indices,
        drop=False,
        satellite_mission=satellite_mission,
    )

    return ds


def median_wrapper(ds):
    """Calculate median"""

#     ds = ds.median(dim="time")
    ds = ds.median(dim="time",skipna=True) # revised to skip contamination from NaNs

    return ds


def mean_wrapper(ds):
    """calculate median"""

#     ds = ds.mean(dim="time")
    ds = ds.mean(dim="time",skipna=True) # revised to skip contamination from NaNs

    return ds


def apply_function_over_custom_times(ds, func, func_name, time_ranges):
    """Apply generic function over an xarray dataset"""

    output_list = []

    for timelabel, timeslice in time_ranges.items():

        if isinstance(timeslice, slice):
            ds_timeslice = ds.sel(time=timeslice)
        else:
            ds_timeslice = ds.sel(time=timeslice, method="nearest")

        ds_modified = func(ds_timeslice)
        
        # rechunk if chunck size changed after mean/median
        

        rename_dict = {
            key: f"{key}_{func_name}_{timelabel}" for key in list(ds_modified.keys())
        }

        ds_modified = ds_modified.rename(name_dict=rename_dict)

        if "time" in list(ds_modified.coords):
            ds_modified = ds_modified.reset_coords().drop_vars(["time", "spatial_ref"])

        output_list.append(ds_modified)

    return output_list


# Define functions to load features
def feature_layers(query):
    """Compute feature layers according to datacube query"""
    
    baseline_query = query.copy() # include to make sure original query isn't modified

    # Connnect to datacube
    dc = datacube.Datacube(app="crop_type_ml")

    # Check query for required time ranges and remove them
    if all(
        [
            key in baseline_query.keys()
            for key in [
                "annual_geomedian_times",
                "semiannual_geomedian_times",
                "monthly_ndvi_time_range",
                "ls_fc_cover_times",
            ]
        ]
    ):
        pass
    else:
        print(
            "Query missing at least one of annual_geomedian_times, semiannual_geomedian_times, monthly_ndvi_time_range or ls_fc_cover_times"
        )
        sys.exit(1)

    # ----------------- STORE TIME RANGES FOR CUSTOM QUERIES -----------------
    # This removes these items from the query so it can be used for loads

    annual_geomedian_times = baseline_query.pop("annual_geomedian_times")
    semiannual_geomedian_times = baseline_query.pop("semiannual_geomedian_times")
    monthly_ndvi_time_range=baseline_query.pop("monthly_ndvi_time_range")
    time_ranges = baseline_query.pop("ls_fc_cover_times")

    # ----------------- DEFINE MEASUREMENTS TO USE FOR EACH PRODUCT -----------------

    s2_measurements = [
        "blue",
        "green",
        "red",
        "nir_1",
        "nir_2",
        "swir_1",
        "swir_2",
        "red_edge_1",
        "red_edge_2",
        "red_edge_3",
    ]

    s2_geomad_measurements = s2_measurements + ["smad", "emad", "bcmad"]
    
    monthly_ndvi_measurments=["ndvi_mean"]

    fc_measurements = ["bs", "pv", "npv", "ue"]

    rainfall_measurements = ["rainfall"]

    slope_measurements = ["slope"]
    
    
    # ----------------- S2 ANNUAL GEOMEDIAN -----------------

    # Update query to use annual_geomedian_times
    ds_annual_geomad_query = baseline_query.copy()
    annual_query_times = list(annual_geomedian_times.values())
    annual_start_date = annual_query_times[0]
    annual_end_date = annual_query_times[-1]
    ds_annual_geomad_query.update({"time": (annual_start_date, annual_end_date)})

    # load s2 annual geomedian
    ds_s2_geomad = dc.load(
        product="gm_s2_annual",
        measurements=s2_geomad_measurements,
        **ds_annual_geomad_query,
    )

    # Calculate band indices
    s2_annual_list = apply_function_over_custom_times(
        ds_s2_geomad, indices_wrapper, "s2", annual_geomedian_times
    )
    
    
    # ----------------- S2 SEMIANNUAL GEOMEDIAN -----------------

    # Update query to use semiannual_geomedian_times
    ds_semiannual_geomad_query = baseline_query.copy()
    semiannual_query_times = list(semiannual_geomedian_times.values())
    semiannual_start_date = semiannual_query_times[0]
    semiannual_end_date = semiannual_query_times[-1]
    ds_semiannual_geomad_query.update({"time": (semiannual_start_date, semiannual_end_date)})

    # load s2 semiannual geomedian
    ds_s2_semiannual_geomad = dc.load(
        product="gm_s2_semiannual",
        measurements=s2_geomad_measurements,
        **ds_semiannual_geomad_query,
    )

    # Calculate band indices
    s2_semiannual_list = apply_function_over_custom_times(
        ds_s2_semiannual_geomad, indices_wrapper, "s2", semiannual_geomedian_times
    )

    #---------Landsat monthly NDVI anomaly--------------
    monthly_ndvi_query=baseline_query.copy()
    monthly_ndvi_query.update({"resampling": "bilinear", "measurements": monthly_ndvi_measurments})
    monthly_ndvi_query.update({"time": monthly_ndvi_time_range})
    # load monthly mean NDVI
    ds_monthly_ndvi=dc.load(product="ndvi_anomaly",**monthly_ndvi_query)
    
    # stack multi-temporal measurements and rename them
    n_time=ds_monthly_ndvi.dims['time']
    list_measurements=list(ds_monthly_ndvi.keys())
    ds_monthly_ndvi_list=[]
    for j in range(len(list_measurements)):
        for k in range(n_time):
            variable_name=list_measurements[j]+'_'+str(k)
            measure_single=ds_monthly_ndvi[list_measurements[j]].isel(time=k).rename(variable_name)
            measure_single=measure_single.reset_coords().drop_vars(["time", "spatial_ref"])
            ds_monthly_ndvi_list.append(measure_single)
            
    # -------- LANDSAT BIMONTHLY FRACTIONAL COVER -----------

    # Update query to suit fractional cover
    fc_query = baseline_query.copy()
    fc_query.update({"resampling": "bilinear", "measurements": fc_measurements})
    
    fc_query_times = list(time_ranges.values())
    fc_start_date = fc_query_times[0].start
    fc_end_date = fc_query_times[-1].stop
    fc_query.update({"time": (fc_start_date, fc_end_date)})

    # load fractional cover
    ds_fc = dc.load(product="fc_ls", collection_category="T1", **fc_query)
    
    # Make a clear (no-cloud) and dry (no-water) pixel mask
    # load wofls
#     ds_wofls = dc.load(product='wofs_ls',
#                 like=ds_fc.geobox,
#                 time=fc_query['time'],
#                 collection_category='T1')
    ds_wofls = dc.load(product='wofs_ls',
            like=ds_fc,
            time=fc_query['time'],
            collection_category='T1') # revised 'like'
    clear_and_dry = masking.make_mask(ds_wofls, dry=True).water
    ds_fc_clear = ds_fc.where(clear_and_dry) # revised: only do masking without removing scenes

#     #keep mostly clear scenes by calculating the number of good pixels per scene and applying a threshold
#     #set a good data fraction
#     min_gooddata = 0.95

#     #keep only the images that are at least as clear as min_gooddata
#     good_slice = clear_and_dry.mean(['x','y']) >= min_gooddata

#     #apply the "clear mask" and filter to just the scenes that are mostly free of cloud and water
# #     ds_fc_clear = ds_fc.where(clear_and_dry).isel(time=good_slice)
#     ds_fc_clear = ds_fc.where(clear_and_dry.isel(time=good_slice)) # to avoid logical bug

#     # Apply median
#     fc_median_list = apply_function_over_custom_times(
#         ds_fc_clear, median_wrapper, "median", time_ranges
#     )

    # Apply mean as median somehow makes dask rechunk
    fc_median_list = apply_function_over_custom_times(
        ds_fc_clear, mean_wrapper, "mean", time_ranges
    )

    # -------- DEM SLOPE -----------
    slope_query = baseline_query.copy()
    slope_query.update(
        {
            "resampling": "bilinear",
            "measurements": slope_measurements,
            "time": "2000-01-01",
        }
    )
    
    # Load slope data and update no data values and coordinates
    ds_slope = dc.load(product="dem_srtm_deriv", **slope_query)

    slope_nodata = -9999.0
    ds_slope = ds_slope.where(ds_slope != slope_nodata, np.nan)

    ds_slope = ds_slope.squeeze("time")#.reset_coords("time", drop=True)

    # ----------------- FINAL MERGED XARRAY -----------------

    # Create a list to keep all items for final merge
    ds_list = []
    ds_list.extend(s2_annual_list)
    ds_list.extend(s2_semiannual_list)
    ds_list.extend(ds_monthly_ndvi_list)
    ds_list.extend(fc_median_list)
    ds_list.append(ds_slope)

    ds_final = xr.merge(ds_list)
    

    return ds_final
