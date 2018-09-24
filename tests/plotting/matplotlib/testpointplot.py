import numpy as np

from holoviews.core.overlay import NdOverlay
from holoviews.element import Points

from .testplot import TestMPLPlot, mpl_renderer
from ..utils import ParamLogStream

try:
    from matplotlib import pyplot
except:
    pass


class TestPointPlot(TestMPLPlot):

    def test_points_non_numeric_size_warning(self):
        data = (np.arange(10), np.arange(10), list(map(chr, range(94,104))))
        points = Points(data, vdims=['z']).opts(plot=dict(size_index=2))
        with ParamLogStream() as log:
            plot = mpl_renderer.get_plot(points)
        log_msg = log.stream.read()
        warning = ('%s: z dimension is not numeric, '
                   'cannot use to scale Points size.\n' % plot.name)
        self.assertEqual(log_msg, warning)

    def test_points_cbar_extend_both(self):
        img = Points(([0, 1], [0, 3])).redim(y=dict(range=(1,2)))
        plot = mpl_renderer.get_plot(img(plot=dict(colorbar=True, color_index=1)))
        self.assertEqual(plot.handles['cbar'].extend, 'both')

    def test_points_cbar_extend_min(self):
        img = Points(([0, 1], [0, 3])).redim(y=dict(range=(1, None)))
        plot = mpl_renderer.get_plot(img(plot=dict(colorbar=True, color_index=1)))
        self.assertEqual(plot.handles['cbar'].extend, 'min')

    def test_points_cbar_extend_max(self):
        img = Points(([0, 1], [0, 3])).redim(y=dict(range=(None, 2)))
        plot = mpl_renderer.get_plot(img(plot=dict(colorbar=True, color_index=1)))
        self.assertEqual(plot.handles['cbar'].extend, 'max')

    def test_points_cbar_extend_clime(self):
        img = Points(([0, 1], [0, 3])).opts(style=dict(clim=(None, None)))
        plot = mpl_renderer.get_plot(img(plot=dict(colorbar=True, color_index=1)))
        self.assertEqual(plot.handles['cbar'].extend, 'neither')

    def test_points_rcparams_do_not_persist(self):
        opts = dict(fig_rcparams={'text.usetex': True})
        points = Points(([0, 1], [0, 3])).opts(plot=opts)
        mpl_renderer.get_plot(points)
        self.assertFalse(pyplot.rcParams['text.usetex'])

    def test_points_rcparams_used(self):
        opts = dict(fig_rcparams={'grid.color': 'red'})
        points = Points(([0, 1], [0, 3])).opts(plot=opts)
        plot = mpl_renderer.get_plot(points)
        ax = plot.state.axes[0]
        lines = ax.get_xgridlines()
        self.assertEqual(lines[0].get_color(), 'red')
    
    def test_points_padding_square(self):
        points = Points([1, 2, 3]).options(padding=0.1)
        plot = mpl_renderer.get_plot(points)
        x_range, y_range = plot.handles['axis'].get_xlim(), plot.handles['axis'].get_ylim()
        self.assertEqual(x_range[0], -0.2)
        self.assertEqual(x_range[1], 2.2)
        self.assertEqual(y_range[0], 0.8)
        self.assertEqual(y_range[1], 3.2)

    def test_curve_padding_square_per_axis(self):
        curve = Points([1, 2, 3]).options(padding=((0, 0.1), (0.1, 0.2)))
        plot = mpl_renderer.get_plot(curve)
        x_range, y_range = plot.handles['axis'].get_xlim(), plot.handles['axis'].get_ylim()
        self.assertEqual(x_range[0], 0)
        self.assertEqual(x_range[1], 2.2)
        self.assertEqual(y_range[0], 0.8)
        self.assertEqual(y_range[1], 3.4)

    def test_points_padding_hard_xrange(self):
        points = Points([1, 2, 3]).redim.range(x=(0, 3)).options(padding=0.1)
        plot = mpl_renderer.get_plot(points)
        x_range, y_range = plot.handles['axis'].get_xlim(), plot.handles['axis'].get_ylim()
        self.assertEqual(x_range[0], 0)
        self.assertEqual(x_range[1], 3)
        self.assertEqual(y_range[0], 0.8)
        self.assertEqual(y_range[1], 3.2)

    def test_points_padding_soft_xrange(self):
        points = Points([1, 2, 3]).redim.soft_range(x=(0, 3)).options(padding=0.1)
        plot = mpl_renderer.get_plot(points)
        x_range, y_range = plot.handles['axis'].get_xlim(), plot.handles['axis'].get_ylim()
        self.assertEqual(x_range[0], -0.2)
        self.assertEqual(x_range[1], 3)
        self.assertEqual(y_range[0], 0.8)
        self.assertEqual(y_range[1], 3.2)

    def test_points_padding_unequal(self):
        points = Points([1, 2, 3]).options(padding=(0.05, 0.1))
        plot = mpl_renderer.get_plot(points)
        x_range, y_range = plot.handles['axis'].get_xlim(), plot.handles['axis'].get_ylim()
        self.assertEqual(x_range[0], -0.1)
        self.assertEqual(x_range[1], 2.1)
        self.assertEqual(y_range[0], 0.8)
        self.assertEqual(y_range[1], 3.2)

    def test_points_padding_nonsquare(self):
        points = Points([1, 2, 3]).options(padding=0.1, aspect=2)
        plot = mpl_renderer.get_plot(points)
        x_range, y_range = plot.handles['axis'].get_xlim(), plot.handles['axis'].get_ylim()
        self.assertEqual(x_range[0], -0.1)
        self.assertEqual(x_range[1], 2.1)
        self.assertEqual(y_range[0], 0.8)
        self.assertEqual(y_range[1], 3.2)

    def test_points_padding_logx(self):
        points = Points([(1, 1), (2, 2), (3,3)]).options(padding=0.1, logx=True)
        plot = mpl_renderer.get_plot(points)
        x_range, y_range = plot.handles['axis'].get_xlim(), plot.handles['axis'].get_ylim()
        self.assertEqual(x_range[0], 0.89595845984076228)
        self.assertEqual(x_range[1], 3.3483695221017129)
        self.assertEqual(y_range[0], 0.8)
        self.assertEqual(y_range[1], 3.2)

    def test_points_padding_logy(self):
        points = Points([1, 2, 3]).options(padding=0.1, logy=True)
        plot = mpl_renderer.get_plot(points)
        x_range, y_range = plot.handles['axis'].get_xlim(), plot.handles['axis'].get_ylim()
        self.assertEqual(x_range[0], -0.2)
        self.assertEqual(x_range[1], 2.2)
        self.assertEqual(y_range[0], 0.89595845984076228)
        self.assertEqual(y_range[1], 3.3483695221017129)

    def test_points_padding_datetime_square(self):
        points = Points([(np.datetime64('2016-04-0%d' % i), i) for i in range(1, 4)]).options(
            padding=0.1
        )
        plot = mpl_renderer.get_plot(points)
        x_range, y_range = plot.handles['axis'].get_xlim(), plot.handles['axis'].get_ylim()
        self.assertEqual(x_range[0], 736054.80000000005)
        self.assertEqual(x_range[1], 736057.19999999995)
        self.assertEqual(y_range[0], 0.8)
        self.assertEqual(y_range[1], 3.2)

    def test_points_padding_datetime_nonsquare(self):
        points = Points([(np.datetime64('2016-04-0%d' % i), i) for i in range(1, 4)]).options(
            padding=0.1, aspect=2
        )
        plot = mpl_renderer.get_plot(points)
        x_range, y_range = plot.handles['axis'].get_xlim(), plot.handles['axis'].get_ylim()
        self.assertEqual(x_range[0], 736054.90000000002)
        self.assertEqual(x_range[1], 736057.09999999998)
        self.assertEqual(y_range[0], 0.8)
        self.assertEqual(y_range[1], 3.2)

    def test_point_color_op(self):
        points = Points([(0, 0, '#000000'), (0, 1, '#FF0000'), (0, 2, '#00FF00')],
                        vdims='color').options(color='color')
        plot = mpl_renderer.get_plot(points)
        artist = plot.handles['artist']
        self.assertEqual(artist.get_facecolors(),
                         np.array([[0, 0, 0, 1], [1, 0, 0, 1], [0, 1, 0, 1]]))

    def test_point_line_color_op(self):
        points = Points([(0, 0, '#000000'), (0, 1, '#FF0000'), (0, 2, '#00FF00')],
                        vdims='color').options(edgecolors='color')
        plot = mpl_renderer.get_plot(points)
        artist = plot.handles['artist']
        self.assertEqual(artist.get_edgecolors(),
                         np.array([[0, 0, 0, 1], [1, 0, 0, 1], [0, 1, 0, 1]]))

    def test_point_fill_color_op(self):
        points = Points([(0, 0, '#000000'), (0, 1, '#FF0000'), (0, 2, '#00FF00')],
                        vdims='color').options(facecolors='color')
        plot = mpl_renderer.get_plot(points)
        artist = plot.handles['artist']
        self.assertEqual(artist.get_facecolors(),
                         np.array([[0, 0, 0, 1], [1, 0, 0, 1], [0, 1, 0, 1]]))

    def test_point_linear_color_op(self):
        points = Points([(0, 0, 0), (0, 1, 1), (0, 2, 2)],
                        vdims='color').options(color='color')
        plot = mpl_renderer.get_plot(points)
        artist = plot.handles['artist']
        self.assertEqual(artist.get_array(), np.array([0, 1, 2]))
        self.assertEqual(artist.get_clim(), (0, 2))

    def test_point_categorical_color_op(self):
        points = Points([(0, 0, 'A'), (0, 1, 'B'), (0, 2, 'A')],
                        vdims='color').options(color='color')
        plot = mpl_renderer.get_plot(points)
        artist = plot.handles['artist']
        self.assertEqual(artist.get_array(), np.array([0, 1, 0]))
        self.assertEqual(artist.get_clim(), (0, 1))

    def test_point_size_op(self):
        points = Points([(0, 0, 1), (0, 1, 4), (0, 2, 8)],
                        vdims='size').options(s='size')
        plot = mpl_renderer.get_plot(points)
        artist = plot.handles['artist']
        self.assertEqual(artist.get_sizes(), np.array([1, 4, 8]))

    def test_point_line_width_op(self):
        points = Points([(0, 0, 1), (0, 1, 4), (0, 2, 8)],
                        vdims='line_width').options(linewidth='line_width')
        plot = mpl_renderer.get_plot(points)
        artist = plot.handles['artist']
        self.assertEqual(artist.get_linewidths(), [1, 4, 8])

    def test_point_marker_op(self):
        points = Points([(0, 0, 'circle'), (0, 1, 'triangle'), (0, 2, 'square')],
                        vdims='marker').options(marker='marker')
        with self.assertRaises(ValueError):
            mpl_renderer.get_plot(points)

    def test_point_alpha_op(self):
        points = Points([(0, 0, 0), (0, 1, 0.2), (0, 2, 0.7)],
                        vdims='alpha').options(alpha='alpha')
        with self.assertRaises(ValueError):
            mpl_renderer.get_plot(points)

    def test_op_ndoverlay_value(self):
        markers = ['d', 's']
        overlay = NdOverlay({marker: Points(np.arange(i))
                             for i, marker in enumerate(markers)},
                            'Marker').options('Points', marker='Marker')
        plot = mpl_renderer.get_plot(overlay)
        for subplot, marker in zip(plot.subplots.values(), markers):
            style = dict(subplot.style[subplot.cyclic_index])
            style = subplot._apply_ops(subplot.current_frame, {}, style)
            self.assertEqual(style['marker'], marker)
