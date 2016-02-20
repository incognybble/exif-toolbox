# By: incognybble
# Created: 7th Feb 2016
# Last modified: 14th Feb 2016

import os

from PIL import Image
import piexif

def remove_gps_exif(photo):
    """Return EXIF without GPS data, along with flag indicating if original
    file had GPS EXIF data. Form: (exif_bytes, gps)

    photo: Original file location.
    exif_bytes: Modified EXIF data.
    gps: Flag indicating if original file had GPS EXIF data.
    """
        
    exif_dict = piexif.load(photo)

    """
    for i in exif_dict["GPS"]:
        print i, piexif.TAGS["GPS"][i]["name"], type(exif_dict["GPS"][i]), exif_dict["GPS"][i]
    """

    gps = False
    if exif_dict["0th"].has_key(34853):
        del exif_dict["0th"][34853] #GPSTag
        del exif_dict["GPS"]
        gps = True

    exif_bytes = piexif.dump(exif_dict)

    return (exif_bytes, gps)

def add_exif(photo, exif_bytes):
    """Add EXIF to EXIF-less photo. Used for copying modified EXIF to
    existing image without overwriting any images. Useful if the existing
    image is different than the original.

    photo: File location of photo to receive EXIF.
    exif_bytes: EXIF data.
    """
    
    piexif.insert(exif_bytes, photo)

def modify_exif(photo, exif_bytes, new_photo=None):
    """Save EXIF to either current file or make a new image.

    photo: Original file location.
    exif_bytes: EXIF data.
    new_photo: New file location. Optional.
    """
    
    if new_photo == None:
        new_photo = photo
        
    im = Image.open(photo)
    im.save(new_photo, "jpeg", exif=exif_bytes)

def remove_gps_folder(folder, new_folder=None, original=True, status_print = False):
    """Remove GPS from EXIF of all jpgs in a folder.

    folder: Location of original folder.
    new_folder: Location of folder for modified images. Optional.
    original: Flag indicating whether to use original image data. Optional.
        Default is True. Alternative would be to insert EXIF into an
        existing image.
    status_print: Flag indicating whether to print current progress.
        Optional. Default is False.
    """
    
    if new_folder == None:
        new_folder = folder
    
    photos = os.listdir(folder)
    photos.sort()
    for photo in photos:
        if os.path.isfile(os.path.join(folder, photo)):
            if (os.path.splitext(photo)[1]).lower() == ".jpg":
                old_file = os.path.join(folder, photo)
                new_file = os.path.join(new_folder, photo)
                (exif_bytes, gps) = remove_gps_exif(old_file)

                if orginal == False:
                    add_exif(new_file, exif_bytes)
                else:
                    modify_exif(new_file, exif_bytes)

                if status_print == True:
                    if gps:
                        print photo
                    else:
                        print photo + " - Nope!"

if __name__ == "__main__":
    pass
