import math
import cairo

from screenlets.options import ColorOption, IntOption, StringOption, FloatOption, FontOption

fft = True

#array for font weight
fontweights = {
  'ultralight' : cairo.FONT_WEIGHT_NORMAL,
  'light'      : cairo.FONT_WEIGHT_NORMAL,
  'normal'     : cairo.FONT_WEIGHT_NORMAL,
  'medium'     : cairo.FONT_WEIGHT_NORMAL,
  'semibold'   : cairo.FONT_WEIGHT_BOLD,
  'bold'       : cairo.FONT_WEIGHT_BOLD,
  'heavy'      : cairo.FONT_WEIGHT_BOLD,
  'ultrabold'  : cairo.FONT_WEIGHT_BOLD,
  'black'      : cairo.FONT_WEIGHT_BOLD,
}

#array for font slant
fontslants = {
  'italic'  : cairo.FONT_SLANT_ITALIC,
  'normal'  : cairo.FONT_SLANT_NORMAL,
  'oblique' : cairo.FONT_SLANT_OBLIQUE,
}
                   
peak_heights = [ 0 for i in range( 256 ) ]
peak_acceleration = [ 0.0 for i in range( 256 ) ]

bar_color = ( 0.91, 0.39, 0.21, 0.65 )
bg_color = ( 0.91, 0.39, 0.21, 0.39 )
peak_color = ( 1.0, 1.0, 1.0, 0.65 )
peak_bg_color = ( 1.0, 1.0, 1.0, 0.39 )

n_cols = 24
col_width = 8
col_spacing = 0

n_rows = 17
row_height = 3
row_spacing = 0

amplified_function = 2
exp_factor = 0.8

text_to_write = 'ubuntu'
text_font = "Ubuntu 72"
text_spacing = 2
left_spacing = 0
bottom_spacing = 0
text_color = ( 0.26, 0.26, 0.24, 0.8 )
scr_width = 50
scr_height = 50

def load_theme ( screenlet ):

	screenlet.update( )

	screenlet.add_option( ColorOption(
		'Impulse', 'bar_color',
		bar_color, 'Bar color',
		'Example options group using color'
	) )

	screenlet.add_option( ColorOption(
		'Impulse', 'peak_color',
		peak_color, 'Peak color',
		'Example options group using color')
	)

	screenlet.add_option( ColorOption(
		'Impulse', 'peak_bg_color',
		peak_bg_color, 'Background Peak color',
		'Example options group using color')
	)

	screenlet.add_option( ColorOption(
		'Impulse', 'bg_color',
		bg_color, 'Background Bar color',
		'Example options group using color')
	)

	screenlet.add_option( IntOption(
		'Impulse', 'n_cols',
		n_cols, 'Number of columns',
		'Example options group using integer',
		min=1, max=256
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'col_width',
		col_width, 'Column width',
		'Example options group using integer',
		min=1, max=256
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'col_spacing',
		col_spacing, 'Column Spacing',
		'Example options group using integer',
		min=0, max=256
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'n_rows',
		n_rows, 'Number of rows',
		'Example options group using integer',
		min=5, max=256
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'row_height',
		row_height, 'Row height',
		'Example options group using integer',
		min=1, max=256
	) )

	screenlet.add_option( IntOption(
		'Impulse', 'row_spacing',
		row_spacing, 'Row Spacing',
		'Example options group using integer',
		min=0, max=256
	) )
		
	screenlet.add_options_group( 'Amplify', 'Select function\n\t0 = None\n\t1 = Sinusoidal\n\t2 = Exponential\n\nand Exopnential factor for Exponential function' )
	
	screenlet.add_option( IntOption(
		'Amplify', 'amplified_function',
		amplified_function, 'Amplified Function Signal ',
		'',
		min=0, max=2
	) )

	screenlet.add_option( FloatOption(
		'Amplify', 'exp_factor',
		exp_factor, 'Exponential Factor',
		'',
		min=0.01, max=1.0, increment=0.01,digits=2
	) )
	
	screenlet.add_options_group( 'Text', 'Change the Text and Format.' )

	screenlet.add_option( StringOption(
		'Text', 'text_to_write',
		text_to_write, 'Text'
		''
	) )

	screenlet.add_option( FontOption(
		'Text','text_font', 
		text_font, 'Text Font', 
		'Example options group using font'
	))

	screenlet.add_option( IntOption(
		'Text', 'left_spacing',
		left_spacing, 'Left Spacing',
		'Example options group using integer',
		min=-50, max=50
	) )

	screenlet.add_option( IntOption(
		'Text', 'bottom_spacing',
		bottom_spacing, 'Bottom Spacing',
		'Example options group using integer',
		min=-50, max=50
	) )

	screenlet.add_option( IntOption(
		'Text', 'text_spacing',
		text_spacing, 'Letter Spacing',
		'Example options group using integer',
		min=-10, max=50
	) )
	
	screenlet.add_option( ColorOption(
		'Text', 'text_color',
		text_color, 'Text color',
		'Example options group using color')
	)

def on_after_set_attribute ( self, name, value, screenlet ):
	setattr( self, name, value )
	screenlet.update( )

def get_audio_value ( sample ):
  #apply amplified function if setted
	factor = sample
	if (amplified_function == 1) :
		factor = math.sin(math.pi/2 * sample)
	elif (amplified_function == 2) :
		factor = math.pow(sample, 1.0 - exp_factor)
	return int( factor * ( n_rows - 2 ) )

def apply_text_font( ctx, font_str ):
  #set font information from string ( E.g. 'Ubuntu Bold Italic 72' )
	txt_split = font_str.split()
	txt_slant = fontslants['normal']
	txt_weigh = fontweights['normal']

  #last info is size
	ctx.set_font_size( int(txt_split[-1]) )
	del txt_split[-1]

  #check if there is weight and slant info in the string
	if (txt_split[-1].lower() in fontslants):
		txt_slant = fontslants[txt_split[-1].lower()]
		del txt_split[-1]
	elif (txt_split[-1].lower() in fontweights):
		txt_weigh = fontweights[txt_split[-1].lower()]
		del txt_split[-1]
	if (txt_split[-1].lower() in fontslants):
		txt_slant = fontslants[txt_split[-1].lower()]
		del txt_split[-1]
	elif (txt_split[-1].lower() in fontweights):
		txt_weigh = fontweights[txt_split[-1].lower()]
		del txt_split[-1]

  #set all the rest as a font string 
	ctx.select_font_face( ' '.join(txt_split), txt_slant, txt_weigh )

def on_draw ( audio_sample_array, cr, screenlet ):

	apply_text_font( cr, text_font )	

  #calculating text width and height
	text_width = 0 
	text_height = 0
	for cx, letter in enumerate( text_to_write ):
		xbearing, ybearing, width, height, xadvance, yadvance = ( cr.text_extents(letter))
		if (letter == ' '):
		  text_width += text_last_width
		else :
		  text_last_width = width
		text_width += width + text_spacing
		text_height = max( text_height, height ) 

  #calculating equalizer width and height
	equal_width = n_cols * ( col_width + col_spacing )
	equal_height = n_rows * ( row_height + row_spacing )
	
  #calculating screen size needed
	scr_width = max(text_width +max(0, left_spacing), equal_width +max(0, -left_spacing) )+10
	scr_height = max(text_height +max(0, -bottom_spacing), equal_height +max(0, bottom_spacing) )+10

  #set new screen size if modified
	if (screenlet.width <> scr_width or screenlet.height <> scr_height):
		if (screenlet.width <> scr_width) :
			screenlet.width = scr_width
		if (screenlet.height <> scr_height) :
			screenlet.height = scr_height
		screenlet.resize(scr_width, scr_height)

  #start draw text
	cr.set_source_rgba( text_color[ 0 ], text_color[ 1 ], text_color[ 2 ], text_color[ 3 ] )
	text_last_width = 0
	left_offset = 0

  #offset of text
	cr.save( )
	cr.translate( max(0,left_spacing),  max(text_height, equal_height-bottom_spacing) )

	for cx, letter in enumerate( text_to_write ):
		xbearing, ybearing, width, height, xadvance, yadvance = ( cr.text_extents(letter))
		cr.move_to(left_offset, 0)
		if (letter == ' '):
		  left_offset += text_last_width
		else :
		  text_last_width = width
		left_offset += width + text_spacing 
		cr.show_text(letter)

  #start draw equalizer
	freq = len( audio_sample_array ) / n_cols
	cr.restore( )

  #offset of equalizer
	cr.translate( max(0,-left_spacing), max(text_height+bottom_spacing, equal_height) )
 
  #draw bar over text
	cr.set_source_rgba( bar_color[ 0 ], bar_color[ 1 ], bar_color[ 2 ], bar_color[ 3 ] )
	for i in range( 0, len( audio_sample_array ), freq ):
		col = i / freq
		rows = get_audio_value (audio_sample_array[ i ] )

		for row in range( 0, rows ):

			cr.rectangle(
				col * ( col_width + col_spacing ),
				0 - row * ( row_height + row_spacing ),
				col_width, -row_height
			)
	cr.set_operator(cairo.OPERATOR_ATOP)
	cr.fill()

  #draw pick over text
	cr.set_source_rgba( peak_color[ 0 ], peak_color[ 1 ], peak_color[ 2 ], peak_color[ 3 ] )
	for i in range( 0, len( audio_sample_array ), freq ):
		col = i / freq
		rows = get_audio_value (audio_sample_array[ i ] )

		if rows > peak_heights[ i ]:
			peak_heights[ i ] = rows
			peak_acceleration[ i ] = 0.0
		else:
			peak_acceleration[ i ] += .1
			peak_heights[ i ] -= peak_acceleration[ i ]

		if peak_heights[ i ] < 0:
			peak_heights[ i ] = 0

		if (peak_heights[ i ] == 0): continue
		cr.rectangle(
			col * ( col_width + col_spacing ),
			0 - peak_heights[ i ] * ( row_height + row_spacing ),
			col_width, -row_height
		)
	cr.set_operator(cairo.OPERATOR_ATOP)
	cr.fill()

  #draw bar out of the text
	cr.set_source_rgba( bg_color[ 0 ], bg_color[ 1 ], bg_color[ 2 ], bg_color[ 3 ] )
	for i in range( 0, len( audio_sample_array ), freq ):
		col = i / freq
		rows = get_audio_value (audio_sample_array[ i ] )

		for row in range( 0, rows ):

			cr.rectangle(
				col * ( col_width + col_spacing ),
				0 - row * ( row_height + row_spacing ),
				col_width, -row_height
			)
	cr.set_operator(cairo.OPERATOR_DEST_OVER)
	cr.fill()

  #draw pick out of the text
	cr.set_source_rgba( peak_bg_color[ 0 ], peak_bg_color[ 1 ], peak_bg_color[ 2 ], peak_bg_color[ 3 ] )
	for i in range( 0, len( audio_sample_array ), freq ):
		col = i / freq
		rows = get_audio_value (audio_sample_array[ i ] )

		if (peak_heights[ i ] == 0): continue
		cr.rectangle(
			col * ( col_width + col_spacing ),
			0 - peak_heights[ i ] * ( row_height + row_spacing ),
			col_width, -row_height
		)
	cr.set_operator(cairo.OPERATOR_DEST_OVER)
	cr.fill()

	cr.fill( )
	cr.stroke( )

