from PIL import Image

def real_size_in(im, dpi):
    # the function image.size() returns the size of an image in pixels
    return [dim / dpi for dim in im.size] # converting to inches

def resampling(im, old_dpi, new_dpi):
    physical_size = real_size_in(im, old_dpi) # Getting the real size of what was captured in the image in inches
    
    # New pixel resolution
    new_pixel_dims = [int(physical_size[0] * new_dpi), int(physical_size[1] * new_dpi)]
    
    # resmpling
    return im.resize(tuple(new_pixel_dims), Image.Resampling.LANCZOS)

def combine_images_horizontally(images, original_mode):
    # Getting the dimensions of the images
    widths, heights = zip(*(i.size for i in images))

    
    #Dimensioning the final image
    total_width = sum(widths)
    max_height = max(heights)

    # Creating it
    combined_im = Image.new(original_mode, (total_width, max_height))

    # Building it
    x_offset = 0
    for im in images:
        combined_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    
    return combined_im

def main():
    images = [] # Will contain all of the generated images
    try:
        im = Image.open("resampling.tif")
    except FileNotFoundError:
        print("Error 'resampling.tif' not found.")
        return

    # Reading dpi of the image
    dpi = im.info.get('dpi', (72, 72))[0] # default of 72 if dpi not found

    print("- Original Image")
    print(f"Definition: {im.size} | Formato: {im.format} | Modo: {im.mode} | DPI: {dpi}")
    print("-" * 20)

    print("(Input 0 to stop)")
    while True:
        try:
            new_dpi_str = input("Resample for the DPI: ")
            new_dpi = int(new_dpi_str)

            if new_dpi == 0:
                break

            resam_im = resampling(im, dpi, new_dpi)
            images.append(resam_im)
            
        except ValueError:
            print("Please, insert a natural number.")
        except Exception as e:
            print(f"Error: {e}")
            break

    if images:
        print("\nCombining all generated images")
        final_image = combine_images_horizontally(images, im.mode)
        
        # Showing the result
        final_image.show()
        
        # Saving the result
        final_image.save("final_image.png")
        print("Photo collage saved as: final_image.png")
    else:
        print("\nNothing to do the collage.")

if __name__ == "__main__":
    main()