"""Download all images from the Wix site into Hugo static/images/ directories."""
import os
import urllib.request

BASE = "https://static.wixstatic.com/media/"
OUT = os.path.join(os.path.dirname(__file__), "static", "images")

# Map: (target_folder, filename) -> wix_media_id
IMAGES = {
    # Hero / slideshow
    ("hero", "hero1.jpg"): "f42095_0ded1f6fabe24fad8ba260cdb40acc64~mv2.jpg",
    ("hero", "hero2.jpg"): "f42095_938c8619ae8344339c7bc078ae1c89f5~mv2.jpg",
    ("hero", "hero3.jpg"): "f42095_636edffa4e854e518c8cfdc37ed6c715~mv2.jpg",

    # PI headshot
    ("team", "jihong_min.jpg"): "f42095_7d387821e0374309b2c660cc5cd8d0d8~mv2.jpg",

    # Publications banner
    ("hero", "publications_banner.jpg"): "f42095_001b3eea3fcb45a38bf9a03ed7195442~mv2.jpg",

    # Research overview and sponsors
    ("research", "research_overview.png"): "f42095_f11ac1bbdca847a689696109c8eb0e87~mv2.png",
    ("research", "sponsors.png"): "f42095_7e59dd7989664967bc2d2de37c29f232~mv2.png",

    # Research topic thumbnails
    ("research", "wearable_sensors.jpg"): "f42095_636edffa4e854e518c8cfdc37ed6c715~mv2.jpg",
    ("research", "battery_free.jpg"): "f42095_479cb9e44ac8465da2561e73471976b4~mv2.jpg",
    ("research", "ingestible.jpg"): "f42095_76be76c6d6a849c3b56289b9cf99baae~mv2.jpg",

    # Research figures
    ("research", "fig_leg_sensors.png"): "f42095_ddfa2758d1df4c8e95d95b4d689402db~mv2.png",
    ("research", "fig_mip_sensors.png"): "f42095_2c220df7ad23423da39341ada955d598~mv2.png",
    ("research", "fig_leg_immunosensors.png"): "f42095_76ce6caebd884983a2feabc8554f1236~mv2.png",
    ("research", "fig_motion_energy.png"): "f42095_6624de914da94f99960dd4b8213356a5~mv2.png",
    ("research", "fig_sweat_energy.png"): "f42095_fe3214a8b7c64a4b956cc5a6857c988e~mv2.png",
    ("research", "fig_light_energy.png"): "f42095_002dd263870248849df0ac08690e72c3~mv2.png",
    ("research", "fig_gi_tract.png"): "f42095_e5c7c67389954d63917d38594b92b546~mv2.png",

    # Journal covers
    ("covers", "nature_electronics_2025.png"): "f42095_c1211a2983fc4f3fa0002b6f586d34ae~mv2.png",
    ("covers", "nature_electronics.png"): "f42095_273f16a0b9b74c8eac60049f885b300c~mv2.png",
    ("covers", "chemical_reviews.webp"): "f42095_018eaf86370748e8a1852535263042eb~mv2.webp",
    ("covers", "nature_bme.png"): "f42095_1b8670755e0b4b61bf5256ba0b375bc7~mv2.png",
    ("covers", "science_robotics.webp"): "f42095_c806c6368af24b5d884a03d3da8622ac~mv2.webp",

    # Gallery thumbnails
    ("gallery", "sweat1.jpg"): "f42095_4e69b77323fd43dd8c9abef5e9b39567~mv2.jpg",
    ("gallery", "sweat2.jpg"): "f42095_a8c04567d798413cb84b6cf25e3eb71b~mv2.jpg",
    ("gallery", "energy1.png"): "f42095_03cbd5a7aa714022a316e4f885ff80a6~mv2.png",
    ("gallery", "energy2.png"): "f42095_50874799b1f44cdba089160f38858853~mv2.png",
    ("gallery", "ingestible1.jpg"): "f42095_4ffd1be966a744e48a7fc0c1a53ad277~mv2.jpg",
    ("gallery", "ingestible2.jpg"): "f42095_5506bee8408746ba9126dd371fe7878a~mv2.jpg",
    ("gallery", "ingestible3.jpg"): "f42095_91c9437f940544f188cad51c3607f4eb~mv2.jpg",
    ("gallery", "ingestible4.jpg"): "f42095_a0f7322c974243129e881037f1fb1c32~mv2.jpg",
}

def main():
    total = len(IMAGES)
    done = 0
    failed = 0
    for (folder, filename), media_id in IMAGES.items():
        dest_dir = os.path.join(OUT, folder)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, filename)
        url = BASE + media_id
        try:
            urllib.request.urlretrieve(url, dest)
            size_kb = os.path.getsize(dest) / 1024
            done += 1
            print(f"  [{done}/{total}] {folder}/{filename} ({size_kb:.0f} KB)")
        except Exception as e:
            failed += 1
            print(f"  FAILED: {folder}/{filename} - {e}")
    print(f"\nDone! {done} downloaded, {failed} failed.")

if __name__ == "__main__":
    main()
