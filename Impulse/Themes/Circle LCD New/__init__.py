import math

from screenlets.options import ColorOption, IntOption, BoolOption

fft = True
bc = (0.0, 0.6, 1.0, 0.4) #body color
tc = (0.0, 0.6, 1.0, 0.8) #top color
cc = tc                   #center color

n_slices = 20 #Angular divisions
n_steps = 20 

slice_spacing = 20
step_spacing = 1

step_width = 4

center_radius = 15

spiral_factor = -15

logaritmic = True
log_factor = 25

delta_theta = 5
#---------------------------------------

center_x = center_radius + (step_width + step_spacing) * n_steps;
center_y = center_x

slice_angle = 2 * math.pi / n_slices

theta = 0

def load_theme( screenlet ):
	screenlet.resize( 2 * center_x, 2 * center_y )

	screenlet.add_option( ColorOption(
		'Impulse', 'bc',
		bc, 'Body color',
		'Color of the inner rings'
	) )

	screenlet.add_option( ColorOption(
		'Impulse', 'tc',
		tc, 'Outer color',
		'Color of the last ring'
	) )

	screenlet.add_option( ColorOption(
		'Impulse', 'cc',
		cc, 'Center color',
		'Color of the center area'
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'n_slices',
		n_slices, 'Number of slices',
		'Number of slices',
		min=3, max=99
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'n_steps',
		n_steps, 'Number of rings',
		'Number of rings',
		min=3, max=100
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'slice_spacing',
		slice_spacing, 'Slice spacing',
		'Spacing betwen slices, represented as a percentage of the bar width',
		min=0, max=99
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'step_spacing',
		step_spacing, 'Ring spacing',
		'Spacing betwen rings',
		min=0, max=100
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'step_width',
		step_width, 'Ring width',
		'Thicknes of each ring',
		min=1, max=20
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'center_radius',
		center_radius, 'Center radius',
		'Radius of the central area',
		min=10, max=100
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'spiral_factor',
		spiral_factor, 'Spiral factor',
		'Spiral aspect. Zero means no spiral look',
		min=-50, max=50
	) )
	
	screenlet.add_option( IntOption(
		'Impulse', 'delta_theta',
		delta_theta, "Rotation speed",
		"speed and direction of the rotation",
		min=-50, max=50	
	) )

	screenlet.add_option( BoolOption(
		'Impulse', 'logaritmic',
		logaritmic, 'Logaritmic amplitude',
		'Show logaritmic scale instead of a linear scale. Beter for low volumes'
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'log_factor',
		log_factor, 'Logaritmic factor',
		'Sensitivity to low volumes',
		min=10, max=100
	) )
	

def on_after_set_attribute ( self, name, value, screenlet ):
	global center_x, center_y, slice_angle, slice_spacing
	
	setattr( self, name, value )
	center_x = center_radius + (step_width + step_spacing) * n_steps;
	center_y = center_x

	slice_angle = 2 * math.pi / n_slices
	
	screenlet.resize(2 * center_x, 2 * center_y)


def on_draw( audio_sample_array, cr, screenlet ):
	global theta
	
	sample_length = len(audio_sample_array)
	
	spiral = 2.0 * math.pi * spiral_factor / 100 / n_steps
	em1 = math.exp(log_factor / 10.0) - 1.0
	slice_angle_stroke = slice_angle * (100 - slice_spacing) / 100;

	#draw central area
	cr.set_source_rgba(cc[0], cc[1], cc[2], audio_sample_array[0])
	cr.arc(center_x, center_y, center_radius, 0, 2 * math.pi)
	cr.fill( )

	#draw rings
	delta_slice_angle = theta;

	cr.set_line_width(step_width)
	for n_slice in range(0, n_slices):
		slice_amp_norm = audio_sample_array[int(n_slice * (sample_length - 1) / (n_slices - 1))]
		if logaritmic:
			#slice_amp_norm = math.log(em1*(audio_sample_array[int(i * l / n_bars)]+1/em1)) / (log_factor / 10)
			slice_amp_norm = math.log(em1*(slice_amp_norm+1/em1)) / (log_factor / 10)

		slice_amp = int((n_steps - 1) * slice_amp_norm)

		#draw inner rings
		delta_slice_angle2 = delta_slice_angle;
		
		cr.set_source_rgba(bc[0], bc[1], bc[2], bc[3])
		for i in range(0, slice_amp):
			cr.arc(
				center_x, center_y,
				center_radius + (step_width + step_spacing) * i,
				delta_slice_angle2,
				delta_slice_angle2 + slice_angle_stroke
			)
			cr.stroke( )
			delta_slice_angle2 = delta_slice_angle2 + spiral

		#draw the outer ring
		cr.set_source_rgba(tc[0], tc[1], tc[2], tc[3])
		cr.arc(
			center_x, center_y,
			center_radius + (step_width + step_spacing) * slice_amp,
			delta_slice_angle2,
			delta_slice_angle2 + slice_angle_stroke
		)
		
		delta_slice_angle = delta_slice_angle + slice_angle
		cr.stroke( )
	theta = theta + delta_theta / 500.0
	if(theta > 2 * math.pi):
		theta = 0

