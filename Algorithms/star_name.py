from photutils.datasets import load_star_image
from astropy.stats import sigma_clipped_stats
from astropy.nddata import Cutout2D
from astropy.wcs import WCS

hdu = load_star_image()
data, true_wcs = hdu.data, WCS(hdu.header)
print(hdu.header)
mean, median, std = sigma_clipped_stats(data, sigma=3.0)


from twirl import find_peaks

xy = find_peaks(data)[0:20]

import numpy as np
import matplotlib.pyplot as plt
from photutils.aperture import CircularAperture

plt.imshow(data, vmin=np.median(data), vmax=3 * np.median(data), cmap="Greys_r")
_ = CircularAperture(xy, r=10.0).plot(color="y")
plt.show()

from astropy.wcs.utils import proj_plane_pixel_scales

fov = (data.shape * proj_plane_pixel_scales(true_wcs))[0]
center = true_wcs.pixel_to_world(*np.array(data.shape) / 2)

from twirl import gaia_radecs
from twirl.geometry import sparsify

all_radecs = gaia_radecs(center, 1.2 * fov)

# we only keep stars 0.01 degree apart from each other
all_radecs = sparsify(all_radecs, 0.01)

from twirl import compute_wcs

# we only keep the 12 brightest stars from gaia
wcs = compute_wcs(xy, all_radecs[0:30], tolerance=10)

from astroquery.simbad import Simbad

# Set up the SIMBAD query
customSimbad = Simbad()
customSimbad.add_votable_fields('typed_id', 'coordinates')  # Adding typed_id and coordinates fields
customSimbad.remove_votable_fields('names')  # Removing default names field

# Perform the query
result_table = customSimbad.query_object("Betelgeuse")

# Extract the star information from the result table
star_name = result_table['MAIN_ID'][0].decode('utf-8')
typed_id = result_table['TYPED_ID'][0].decode('utf-8')
coordinates = result_table['RA_d'][0], result_table['DEC_d'][0]

# Print the star information
print("Star Name:", star_name)
print("Typed ID:", typed_id)
print("Coordinates (RA, DEC):", coordinates)



# plotting to check the WCS
radecs_xy = np.array(wcs.world_to_pixel_values(all_radecs))
result = plt.imshow(data, vmin=np.median(data), vmax=3 * np.median(data), cmap="Greys_r")
_ = CircularAperture(radecs_xy, 5).plot(color="y", alpha=0.5)
names = ["Andromeda"
"Antlia",
"Apus",
"Aquarius",
"Aquila",
"Ara",
"Aries",
"Auriga",
"Boötes",
"Caelum",
"Camelopardalis",
"Cancer",
"Canes Venatici",
"Canis Major",
"Canis Minor",
"Capricornus",
"Carina",
"Cassiopeia",
"Centaurus",
"Cepheus",
"Cetus",
"Chamaeleon",
"Circinus",
"Columba",
"Coma Berenices",
"Corona Australis",
"Corona Borealis",
"Corvus",
"Crater",
"Crux",
"Cygnus",
"Delphinus",
"Dorado",
"Draco",
"Equuleus",
"Eridanus",
"Fornax",
"Gemini",
"Grus",
"Hercules",
"Horologium",
"Hydra",
"Hydrus",
"Indus",
"Lacerta",
"Leo",
"Leo Minor",
"Lepus",
"Libra",
"Lupus",
"Lynx",
"Lyra",
"Mensa",
"Microscopium",
"Monoceros",
"Musca",
"Norma",
"Octans",
"Ophiuchus",
"Orion",
"Pavo",
"Pegasus",
"Perseus",
"Phoenix",
"Pictor",
"Pisces",
"Piscis Austrinus",
"Puppis",
"Pyxis",
"Reticulum",
"Sagitta",
"Sagittarius",
"Scorpius",
"Sculptor",
"Scutum",
"Serpens",
"Sextans",
"Taurus",
"Telescopium",
"Triangulum",
"Triangulum Australe",
"Tucana",
"Ursa Major",
"Ursa Minor",
"Vela",
"Virgo",
"Volans",
"Vulpecula"
]
for i, (x, y) in enumerate(radecs_xy):
    if i % 10 == 0:
        plt.text(x, y, f"{names[(i+1) % len(names)]}", color='w', fontsize=4 , ha='center', va='center')

plt.savefig('plot.png')  # Specify the filename and extension you prefer


# plt.imsave('output.png',result)

plt.show()

