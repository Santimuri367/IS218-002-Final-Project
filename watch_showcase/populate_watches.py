# populate_watches.py
#!/usr/bin/env python
import os
import django
import decimal
import shutil
# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_showcase.settings')
django.setup()
from products.models import Watch, WatchGroup
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.files import File
# populate_watches.py 
def create_watches():
    watches = [
        {
            'brand': 'Rolex',
            'name': 'Submariner 124060',
            'description': 'The Rolex Submariner 124060 is a quintessential dive watch, known for its robust stainless steel construction, 41mm case, and water resistance up to 300 meters. It features a black dial with luminescent hour markers and a unidirectional rotatable bezel. The watch is powered by Rolex\'s Caliber 3230 movement, offering precision and reliability.',
            'history': 'The Rolex Submariner is one of the most iconic dive watches in history, first introduced in 1953. It has been worn by professional divers, military personnel, and featured in numerous James Bond films.',
            'price': decimal.Decimal('11138.00'),
            'retail_price': decimal.Decimal('9200.00'),
            'model_number': '124060',
            'image_filename': '124060-0001-ny.png.webp'
        },
        {
            'brand': 'Omega',
            'name': 'Speedmaster Professional Moonwatch',
            'description': 'The Omega Speedmaster Professional Moonwatch is renowned for its association with NASA\'s lunar missions. It features a 42mm stainless steel case, black dial with chronograph functions, and a hesalite crystal. The manual-winding Caliber 1861 movement powers the watch, which has a 48-hour power reserve.',
            'history': 'The Omega Speedmaster was the first watch worn on the moon during the Apollo 11 mission in 1969. It has been a part of every NASA manned space mission since.',
            'price': decimal.Decimal('5750.00'),
            'retail_price': decimal.Decimal('6300.00'),
            'model_number': '311.30.42.30.01.005',
            'image_filename': '12330015_1.jpg'
        },
        {
            'brand': 'Seiko',
            'name': 'Prospex "Turtle" SRPE03',
            'description': 'The Seiko Prospex "Turtle" SRPE03 is a popular dive watch featuring a distinctive cushion-shaped 45mm stainless steel case. It boasts a black dial with luminous hands and markers, a day-date display, and is water-resistant up to 200 meters. The automatic Caliber 4R36 movement offers a 41-hour power reserve.',
            'history': 'The Seiko Turtle nickname comes from its cushion case shape. The original version (6309) was produced from 1976 to 1988 and became a favorite among divers for its reliability and affordability.',
            'price': decimal.Decimal('450.00'),
            'retail_price': decimal.Decimal('525.00'),
            'model_number': 'SRPE03',
            'image_filename': 'Seiko-Prospex-SRPE03-Mens-Watch-King-Turtle-Silver-Stainless-Steel_10b8877c-d6eb-47d6-aeec-70d983bb1a47.f233eb85a6b34e56cf7bf3390bac3868.jpeg.webp'
        },
        {
            'brand': 'Tissot',
            'name': 'Seastar 1000 Powermatic 80',
            'description': 'The Tissot Seastar 1000 Powermatic 80 is a Swiss-made dive watch with a 43mm stainless steel case and a unidirectional bezel. It features a blue dial with luminous markers, date display, and is water-resistant up to 300 meters. The Powermatic 80 movement provides an impressive 80-hour power reserve.',
            'history': 'Tissot has been manufacturing watches since 1853, making it one of the oldest Swiss watch brands. The Seastar collection represents their professional diving timepieces.',
            'price': decimal.Decimal('650.00'),
            'retail_price': decimal.Decimal('725.00'),
            'model_number': 'T120.407.11.041.00',
            'image_filename': '51oFrXn4mSL._AC_UY900_.jpg'
        },
        {
            'brand': 'Hamilton',
            'name': 'Khaki Field Mechanical',
            'description': 'The Hamilton Khaki Field Mechanical is a military-inspired watch featuring a 38mm stainless steel case, black dial with white Arabic numerals, and a durable NATO strap. It is powered by the H-50 hand-wound movement, offering an 80-hour power reserve. The watch is known for its rugged design and reliability.',
            'history': 'Hamilton watches have a strong military heritage, having supplied timepieces to the US Armed Forces. The Khaki Field collection is inspired by the military watches Hamilton produced during WWII.',
            'price': decimal.Decimal('450.00'),
            'retail_price': decimal.Decimal('495.00'),
            'model_number': 'H69439931',
            'image_filename': 'h69439931.png.avif'
        },
        {
            'brand': 'Tag Heuer',
            'name': 'Monaco Calibre 11',
            'description': 'The Tag Heuer Monaco Calibre 11 is an iconic chronograph, famously associated with Steve McQueen in the 1971 film "Le Mans." It features a distinctive square 39mm stainless steel case, a blue dial with two white sub-dials, and a date display at 6 o\'clock. The watch is powered by the automatic Calibre 11 movement and offers water resistance up to 100 meters.',
            'history': 'The Monaco was revolutionary when introduced in 1969 as one of the first automatic chronographs and the first square water-resistant watch. It gained fame when worn by Steve McQueen in the film "Le Mans."',
            'price': decimal.Decimal('5250.00'),
            'retail_price': decimal.Decimal('5900.00'),
            'model_number': 'CAW211P.FC6356',
            'image_filename': '71A-TS0VFQL._AC_UY1000_.jpg'
        },
        {
            'brand': 'Breitling',
            'name': 'Navitimer B01 Chronograph',
            'description': 'The Breitling Navitimer B01 Chronograph is a legendary pilot\'s watch, renowned for its intricate slide rule bezel used for aviation calculations. It boasts a 43mm stainless steel case, black dial with three contrasting sub-dials, and luminescent hands and markers. The watch houses the in-house Breitling Manufacture Caliber 01, offering a power reserve of approximately 70 hours.',
            'history': 'The Navitimer was introduced in 1952 and became a favorite among pilots due to its circular slide rule functionality, allowing them to perform various flight calculations on the wrist.',
            'price': decimal.Decimal('7500.00'),
            'retail_price': decimal.Decimal('8300.00'),
            'model_number': 'AB0127211B1P1',
            'image_filename': 'breitling_navitimer_b01_chronograph_46_green_dial_and_stainless_steel_bracelet_watch__46mm__ab0137241l1a1-1-20297784-hx8f132ef9_1.jpg'
        },
        {
            'brand': 'Panerai',
            'name': 'Luminor Base Logo',
            'description': 'The Panerai Luminor Base Logo is a minimalist yet bold timepiece, characterized by its cushion-shaped 44mm stainless steel case and the iconic crown-protecting bridge. It features a black dial with luminous Arabic numerals and hour markers. The watch is powered by the hand-wound P.6000 caliber, providing a 72-hour power reserve and is water-resistant up to 100 meters.',
            'history': 'Panerai originally supplied watches to the Italian Navy\'s elite frogman unit. The crown protection bridge (or "crown guard") is a signature Panerai design element that was patented in 1956.',
            'price': decimal.Decimal('4250.00'),
            'retail_price': decimal.Decimal('5000.00'),
            'model_number': 'PAM00774',
            'image_filename': 'panerai-luminor-base-logo-acciaio-black-dial-mens-watch-pam01000-luxury-swiss-watches-479.jpg'
        },
        {
            'brand': 'Devaco',
            'name': 'Blue Elegance',
            'description': 'The Devaco Blue Elegance features a stunning blue sunburst dial with rose gold-tone indices and hands. It has a slim 40mm rose gold-tone case paired with a genuine blue leather strap. This dress watch includes a date function and is perfect for formal occasions.',
            'history': 'Devaco is an up-and-coming watch brand known for their elegant designs and quality craftsmanship at accessible price points.',
            'price': decimal.Decimal('350.00'),
            'retail_price': decimal.Decimal('399.00'),
            'model_number': 'DE-BL-40-RG',
            'image_filename': 'devaco-blue.jpg'
        },
    ]
    media_dir = os.path.join(os.getcwd(), 'media', 'watches')
    os.makedirs(media_dir, exist_ok=True)
    # Create watches
    for watch_data in watches:
        watch, created = Watch.objects.get_or_create(
            brand=watch_data['brand'],
            name=watch_data['name'],
            defaults={
                'description': watch_data['description'],
                'history': watch_data['history'],
                'price': watch_data['price'],
                'retail_price': watch_data['retail_price'],
                'model_number': watch_data['model_number'],
            }
        )
        image_filename = watch_data['image_filename']
        image_path = os.path.join(media_dir, image_filename)
        if os.path.exists(image_path):
            file_size = os.path.getsize(image_path) 
            if file_size > 1000:
                if watch.image:
                    try:
                        watch.image.delete(save=False)
                    except:
                        pass
                with open(image_path, 'rb') as f:
                    watch.image.save(image_filename, File(f), save=True)
                print(f"Updated image for {watch.brand} {watch.name} with {image_filename} ({file_size} bytes)")
            else:
                print(f"Warning: Image for {watch.brand} {watch.name} is too small ({file_size} bytes). It might not be a valid image.")
        else:
            print(f"Image file not found for {watch.brand} {watch.name}: {image_path}")
        if created:
            print(f"Created watch: {watch.brand} {watch.name}")
        else:
            print(f"Updated watch: {watch.brand} {watch.name}")
def create_groups():
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        admin_user.set_password('adminpassword')
        admin_user.save()
        print("Created admin user")
    brand_groups = [
        {
            'name': 'Rolex Enthusiasts',
            'description': 'A group for discussing Rolex watches, history, collecting advice, and new releases.'
        },
        {
            'name': 'Omega Fans',
            'description': 'For admirers of Omega timepieces, including Speedmaster, Seamaster, and other iconic collections.'
        },
        {
            'name': 'Seiko Collectors',
            'description': 'A community for fans of Seiko watches from affordable dive watches to Grand Seiko luxury pieces.'
        },
        {
            'name': 'Tag Heuer Discussion',
            'description': 'Discuss Tag Heuer\'s rich motorsport heritage, iconic models, and contemporary offerings.'
        },
    ]
    # Create brand groups
    for group_data in brand_groups:
        group, created = WatchGroup.objects.get_or_create(
            name=group_data['name'],
            defaults={
                'description': group_data['description'],
                'admin': admin_user,
                'slug': slugify(group_data['name']),
            }
        )
        if created:
            group.members.add(admin_user)
            print(f"Created group: {group.name}")
        else:
            print(f"Group already exists: {group.name}")
    # Specialized interest groups
    specialized_groups = [
        {
            'name': 'First-Time Buyer Help Group',
            'description': 'A supportive community for those new to watches. Get advice on your first purchase, learn watch basics, and find the perfect timepiece for your budget.',
            'slug': 'first-time-buyer-help',
        },
        {
            'name': 'Dress Watch Enthusiasts',
            'description': 'For lovers of elegant timepieces. Discuss classic styling, thin profiles, and the perfect watch to complement formal attire.',
            'slug': 'dress-watch-enthusiasts',
        },
        {
            'name': 'Classic/Vintage Watch Enthusiasts',
            'description': 'Dedicated to vintage and classical timepieces. Share restoration tips, discuss historical significance, and showcase your vintage finds.',
            'slug': 'vintage-watch-enthusiasts',
        },
        {
            'name': 'Up-and-Coming Brands Talk',
            'description': 'Discover emerging watchmakers and microbrand innovations. Discuss new players disrupting the traditional watch market.',
            'slug': 'upcoming-brands-talk',
        },
        {
            'name': 'DIY Builds/Modifications',
            'description': 'For hands-on enthusiasts who enjoy modifying or building watches. Share your projects, techniques, and custom creations.',
            'slug': 'diy-builds-modifications',
        },
        {
            'name': 'General Discourse',
            'description': 'An open forum for all watch-related topics. Industry news, collecting philosophy, watch spotting, and more.',
            'slug': 'general-discourse',
        },
    ]
    # Create specialized groups
    for group_data in specialized_groups:
        group, created = WatchGroup.objects.get_or_create(
            slug=group_data['slug'],
            defaults={
                'name': group_data['name'],
                'description': group_data['description'],
                'admin': admin_user,
            }
        )
        if created:
            group.members.add(admin_user)
            print(f"Created group: {group.name}")
        else:
            print(f"Group already exists: {group.name}")
if __name__ == '__main__':
    print("Starting watch showcase population script...")
    create_watches()
    create_groups()
    print("Population complete!")