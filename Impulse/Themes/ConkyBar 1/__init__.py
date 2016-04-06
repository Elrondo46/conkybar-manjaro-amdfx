from screenlets.options import ColorOption, IntOption

fft = True

co = ( 0.09, 0.57, 0.81, 0.9 )

n_bars = 174
bar_width = 10
bar_spacing = 1

max_height = 125

def load_theme( screenlet ):
	screenlet.resize( n_bars * (bar_width + bar_spacing), max_height )

	screenlet.add_option( ColorOption(
		'Impulse', 'co',
		co, 'Color',
		'The color of the bars'
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'n_bars',
		n_bars, 'Number of bars',
		'The number of bars',
		min=1, max=1920
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'bar_width',
		bar_width, 'Bar width',
		'The width of a bar',
		min=1, max=1920
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'bar_spacing',
		bar_spacing, 'Bar spacing',
		'The spacing between the bars, 0 = none',
		min=0, max=1920
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'max_height',
		max_height, 'Maximum bar height',
		'The height of the bars.',
		min=1, max=1080
	) )


def on_after_set_attribute ( self, name, value, screenlet ):
	setattr( self, name, value )
	screenlet.resize( n_bars * (bar_width + bar_spacing), max_height * 2)

def on_draw( audio_sample_array, cr, screenlet ):

	l = len( audio_sample_array )

	# Draw bars
	cr.set_source_rgba( co[ 0 ], co[ 1 ], co[ 2 ], co[ 3 ] )
	#for i in range( 0, l, l / n_bars ):
	for i in range( 0, l ):

		bar_height = audio_sample_array[ i ] * max_height + 2

		cr.rectangle(
			( bar_width + bar_spacing ) * ( i / ( l / n_bars ) ),
			max_height - bar_height,
			bar_width,
			bar_height
		)

	cr.fill()
	cr.stroke()

def crop_audio_samples(self, audio_sample_array, nr_bars):
	l = len( audio_sample_array )







