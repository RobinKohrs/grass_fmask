# PyWPS_NDVI_changeIndice

import os

from pywps import Process, LiteralInput, LiteralOutput

__author__ = 'Robin'

class ndvi_index(Process):
    def __init__(self):
        inputs = [LiteralInput('start', 'Start date (eg. 2019-03-01)',
                               data_type='string'),
                  LiteralInput('end', 'End date (eg. 2019-04-01)',
                               data_type='string'),
                  LiteralInput('start2', 'Start date 2 (eg. 2019-03-01)',
                               data_type='string'),
                  LiteralInput('end2', 'End date 2 (eg. 2019-04-01)',
                               data_type='string'),     

        ]
        outputs = [LiteralOutput('stats', 'Computed ndvi statistics',
                                 data_type='string')
        ]

        super(ndvi_index, self).__init__(
            self._handler,
            identifier='ndvi',
            version='0.1',
            title="Sentinel-2 NDVI Calculator",
            abstract='The Process will compute the average NDVI ' \
                      'for a given time-period over an area near Jena',
            profile='',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True,
            grass_location="C:\Sentinel2Project\GrassGIS\PERMANENT"
        )

    def check_date(self, date_str):
        from datetime import datetime

        d = datetime.strptime(date_str, '%Y-%m-%d')
        if d.year != 2019:
            #raise Exception("Only year 2019 allowed")
            pass

    def _handler(self, request, response):
        from subprocess import PIPE
        print("IM HERE")
        import grass.script as gs
        from grass.pygrass.modules import Module
        from grass.exceptions import CalledModuleError

        ######## Date 1
        start = request.inputs['start'][0].data
        end = request.inputs['end'][0].data
        self.check_date(start)
        self.check_date(end)

        ####### Date 2
        start2 = request.inputs['start2'][0].data
        end2 = request.inputs['end2'][0].data
        self.check_date(start2)
        self.check_date(end2)

        output1 = 'ndvi1'
        output2 = "ndvi2"

        # be silent
        os.environ['GRASS_VERBOSE'] = '0'

        # need to set computation region (would be nice g.region strds or t.region)
        #Module('g.region', raster='c_0')
        try:
            Module('t.rast.series',
                   input='ndvi@PERMANENT',
                   output=output1,
                   method='average',
                   where="start_time > '{start}' and start_time < '{end}'".format(
                       start=start, end=end
                   ))
            Module('t.rast.series',
                   input='ndvi@PERMANENT',
                   output=output2,
                   method='average',
                   where="start_time > '{start}' and start_time < '{end}'".format(
                       start=start2, end=end2
                   ))
        except CalledModuleError:
            raise Exception('Unable to compute statistics')

#         ret = Module('r.univar',
#                      flags='g',
#                      map=output1,
#                      stdout_=PIPE
#         )
#         ret2 = Module('r.univar',
#                      flags='g',
#                      map=output2,
#                      stdout_=PIPE
#         )
#
#         stats = gs.parse_key_val(ret.outputs.stdout)
#         stats2 = gs.parse_key_val(ret2.outputs.stdout)
#
#         outstr = 'Min1: {0:.1f};Max1: {1:.1f};Mean1: {2:.4f}; \n Min2 {0:.1f};Max2: {1:.1f}; Mean2: {2:.4f}'.format(
#             float(stats['min']), float(stats['max']), float(stats['mean']), float(stats2["min"]), float(stats2["max"]), float(stats2["mean"]))
#
#         response.outputs['stats'].data = outstr
#
#         return None

        try:
            Module('r.mapcalc',
                   expression='"changeIndice = abs(output1 - output2)"')
            Module('r.recode',
                   input='changeIndice',
                   output='changeIndice_class_rast',
                   rules="-",
                   # classes: -1 - 0.2; 0.2 - 0.6; 0.6 - 1
                   stdin_="-1:0.2:1\n0.2:0.6:2\n0.6:1:3")
            Module('r.to.vect',
                   flags='sv',
                   input='changeIndice_class_rast',
                   output='changeIndice_class_vect',
                   type = "area")
            Module('v.clean',
                   input='changeIndice_class_vect',
                   output='changeIndice_class_vect',
                   tool='rmarea',
                   threshold='1600')

        except CalledModuleError:
            raise Exception('Unable to compute statistics')

        ret = Module('v.rast.stats',
                     flags='c',
                     map='changeIndice_class_vect',
                     raster='changeIndice_class_rast',
                     column_prefix='statistic',
                     method='number, null_cells, minimum, maximum, average')

        stats = gs.parse_key_val(ret.outputs.stdout)

        outstr = 'Number: {0:.4e};Null_Cells: {1:.4e}; Min: {2:.4f}; Max: {3:.4f}; Mean: {4:.4f}'.format(
            float(stats['number']), float(stats['null_cells']), float(stats['minimum'], float(stats['maximum'], float(stats['average'])

        response.outputs['stats'].data = outstr

        return response