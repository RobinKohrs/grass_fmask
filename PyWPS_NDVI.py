# PyWPS_NDVI

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
            grass_location="/home/robin/grassdata/jena_roda"
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

        output1 = 'ndvi1'

        ####### Date 2
        start2 = request.inputs['start2'][0].data
        end2 = request.inputs['end2'][0].data
        self.check_date(start2)
        self.check_date(end2)

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

        except CalledModuleError:
            raise Exception('Unable to compute statistics')

        ret = Module('r.univar',
                     flags='g',
                     map=output1,
                     stdout_=PIPE
        )

        stats = gs.parse_key_val(ret.outputs.stdout)

        outstr1 = 'Min1: {0:.1f};Max1: {1:.1f};Mean1: {2:.4f}'.format(
            float(stats['min']), float(stats['max']), float(stats['mean'])

        try:
            Module('t.rast.series',
                   input='ndvi@PERMANENT',
                   output=output2,
                   method='average',
                   where="start_time > '{start}' and start_time < '{end}'".format(
                       start=start2, end=end2
            ))

        except CalledModuleError:
            raise Exception('Unable to compute statistics')

        ret = Module('r.univar',
                     flags='g',
                     map=output2,
                     stdout_=PIPE
        )

        stats2 = gs.parse_key_val(ret.outputs.stdout)

        outstr2 = 'Min1: {0:.1f};Max1: {1:.1f};Mean1: {2:.4f}'.format(
            float(stats2['min']), float(stats2['max']), float(stats2['mean'])

        response.outputs['stats'].data = outstr1
        response.outputs['stats2'].data = outstr2

        return response
