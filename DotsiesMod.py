import cairo
import itertools

def get_parsed_text(text,cols):
    new_text=[[]]
    for i in text.split():
        if (len(new_text[-1])+len(i))>cols:
            new_text.append([])
        new_text[-1]+=i
        if len(new_text)!=cols:
            new_text[-1]+=" "
    return new_text

def draw(text,file_format='png',file_name="output",square_size=4,cols=50,interline=True):
    text=text.lower()
    
    valid_symbols=" .?,-abcdefghijklmnopqrs'tuvwxyz"
    valid_symbol_set=set(valid_symbols)
    symbol_to_pixels=dict(zip(valid_symbols,itertools.product((0,1),repeat=5)))
    print(symbol_to_pixels)
    
    clear_text="".join([symbol for symbol in text if symbol in valid_symbol_set])
    
    parsed_text=get_parsed_text(clear_text,cols)
    for line in parsed_text:
        print("".join(line))
    
    if interline:
        rows=len(parsed_text)*6-1
        multiplier=6
    else:
        rows=len(parsed_text)*5
        multiplier=5
    
    # Set up the image surface (width, height)
    if file_format == 'svg':
        # SVG surface for SVG output
        width, height = square_size*cols,square_size*rows
        surface = cairo.SVGSurface(file_name+".svg", width, height)
    else:
        # PNG surface for PNG output (default)
        width, height = square_size*cols,square_size*rows
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    
    ctx = cairo.Context(surface)
    
    # Fill background
    ctx.set_source_rgb(1,1,1)  # RGB for white
    ctx.rectangle(0, 0, width, height)  # Full canvas
    ctx.fill()
    
    ctx.set_source_rgb(0,0,0)  # Set color to black
    
    for row in range(len(parsed_text)):
        for col in range(len(parsed_text[row])):
            for idx,is_one in enumerate(symbol_to_pixels[parsed_text[row][col]]):
                if is_one==1:
                    ctx.rectangle(col*square_size,((row*multiplier+idx)*square_size),square_size,square_size)
                    ctx.fill()
    ...
    
    # Save the output based on the chosen file format
    if file_format == 'svg':
        print(f"SVG saved as '{file_name}.svg'")
    else:
        surface.write_to_png(file_name+".png")
        print(f"PNG saved as '{file_name}.png'")


text="""I met a traveller from an antique land, 
Who said, 'Two vast and trunkless legs of stone 
Stand in the desert. Near them, on the sand, 
Half sunk, a shattered visage lies, whose frown, 
And wrinkled lip, and sneer of cold command, 
Tell that its sculptor well those passions read 
Which yet survive, stamped on these lifeless things, 
The hand that mocked them, and the heart that fed; 
And on the pedestal these words appear: 
'My name is Ozymandias, king of kings: 
Look on my works, ye Mighty, and despair!' 
Nothing beside remains. Round the decay 
Of that Colossal Wreck, boundless and bare, 
The lone and level sands stretch far away.' """
draw(text,file_format="svg", cols=80,square_size=1,interline=True)