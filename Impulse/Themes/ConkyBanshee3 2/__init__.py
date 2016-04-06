import math

from screenlets.options import ColorOption, IntOption

fft = True

cc = ( 0.09, 0.57, 0.81, 0.8 )
cc_peak = ( 1.0, 1.0, 1.0, 0.65 )

n_circle_bars = 16
radius = 5
inner_radius = 10

arc_width = 2
arc_spacing = 3

inner_circle_bar = 1

def load_theme( screenlet ):
	screenlet.resize( (radius + arc_spacing) * 2, (radius + arc_spacing) * 2 )

	screenlet.add_option( ColorOption(
		'Impulse', 'cc',
		cc, 'Arc color',
		'Set the color of the arcs'
	) )

	screenlet.add_option( ColorOption(
		'Impulse', 'cc_peak',
		cc_peak, 'Peak arc color',
		'Set the color of the peak arc'
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'inner_circle_bar',
		inner_circle_bar, 'Inner circle arc color',
		'Boolean to make the inner circle the same as the arc color or peak arc color. 0 = bar, 1 = peak color. If no music is playing this determins the arc color.',
		min=0, max=1
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'n_circle_bars',
		n_circle_bars, 'Number of bars on the circle',
		'The number of bars',
		min=1, max=256
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'radius',
		radius, 'Outer circle radius',
		'The radius of the circle',
		min=45, max=544
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'inner_radius',
		inner_radius, 'Inner circle radius',
		'The radius of the inner circle',
		min=1, max=500
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'arc_width',
		arc_width, 'Arc width',
		'The width of the arcs',
		min=1, max=100
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'arc_spacing',
		arc_spacing, 'Arc spacing',
		'The space between the arcs',
		min=1, max=100
	) )


def on_after_set_attribute ( self, name, value, screenlet ):
	setattr( self, name, value )
	screenlet.resize( (radius + arc_spacing) * 2, (radius + arc_spacing) * 2)

def on_draw( audio_sample_array, cr, screenlet ):

	l = len( audio_sample_array )

	# Draw arc's
	cr.set_line_width( arc_width )
	for i in range( 0, l, l / n_circle_bars ):

		cr.set_source_rgba( cc[ 0 ],  cc[ 1 ],  cc[ 2 ],  cc[ 3 ] )
		bar_height = audio_sample_array[ i ] * radius + arc_spacing

		# Draw arcs
		for j in range( 0, int( bar_height / arc_spacing ) - 1):
			cr.arc(
				radius,
				radius,
				inner_radius + j * arc_spacing,
				( math.pi*2 / n_circle_bars ) * ( i / ( l / n_circle_bars ) ),
				( math.pi*2 / n_circle_bars ) * ( i / ( l / n_circle_bars ) + 1 ) - .05
			)
			cr.stroke()

		# Draw peak arc
		if inner_circle_bar == 1:
			cr.set_source_rgba( cc_peak[ 0 ],  cc_peak[ 1 ],  cc_peak[ 2 ],  cc_peak[ 3 ] )
		cr.arc(
			radius,
			radius,
			inner_radius + bar_height,
			( math.pi*2 / n_circle_bars ) * ( i / ( l / n_circle_bars ) ),
			( math.pi*2 / n_circle_bars ) * ( i / ( l / n_circle_bars ) + 1 ) - .05
		)
		cr.stroke()
