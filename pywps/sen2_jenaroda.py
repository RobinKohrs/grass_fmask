import os

from pywps import Process, LiteralInput, LiteralOutput

__author__ = 'Robin'

class Sen2_index(Process):
    def __init__(self):
        inputs = [LiteralInput('start', 'Start date (eg. 2019-03-01)',
                               data_type='string'),
                  LiteralInput('end', 'End date (eg. 2019-04-01)',
                               data_type='string')
        ]
        outputs = [LiteralOutput('stats', 'Computed ndvi statistics',
                                 data_type='string')
        ]

        super(Sen2_index, self).__init__(
            self._handler,
            identifier='sen2_index',
            version='0.1',
            title="Sentinel-2 NDVI Calculator",
            abstract='The Process will compute the average NDVI ' \
                      'for a given time-preiod over an area near Jena',
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
            raise Exception("Only year 2019 allowed")

    def _handler(self, request, response):
        from subprocess import PIPE

        import grass.script as gs
        from grass.pygrass.modules import Module
        from grass.exceptions import CalledModuleError
        
        start = request.inputs['start'][0].data
        end = request.inputs['end'][0].data
        self.check_date(start)
        self.check_date(end)

        output = 'ndvi'
        
        # be silent
        os.environ['GRASS_VERBOSE'] = '0'

        # need to set computation region (would be nice g.region strds or t.region)
        #Module('g.region', raster='c_0')
        try:
            Module('t.rast.series',
                   input='ndvi@PERMANENT',
                   output=output,
                   method='average',
                   where="start_time > '{start}' and start_time < '{end}'".format(
                       start=start, end=end
            ))
        except CalledModuleError:
            raise Exception('Unable to compute statistics')

        ret = Module('r.univar',
                     flags='g',
                     map=output,
                     stdout_=PIPE
        )
        stats = gs.parse_key_val(ret.outputs.stdout)
        
        outstr = 'Min: {0:.1f};Max: {1:.1f};Mean: {2:.1f}'.format(
            float(stats['min']), float(stats['max']), float(stats['mean'])
        )
        response.outputs['stats'].data = outstr

        return response 
