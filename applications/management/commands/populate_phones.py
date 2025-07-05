from django.core.management.base import BaseCommand
from applications.models import Phone

class Command(BaseCommand):
    help = 'Populate database with comprehensive iPhone price list from iPhone 11 to iPhone 16 Pro Max'

    def handle(self, *args, **options):
        # Clear existing phones
        Phone.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared existing phones'))

        # iPhone 11 Series
        iphone_11_models = [
            {'name': 'iPhone 11', 'model': 'A2111', 'storage': '64GB', 'color': 'Black', 'price': 7500},
            {'name': 'iPhone 11', 'model': 'A2111', 'storage': '64GB', 'color': 'White', 'price': 7500},
            {'name': 'iPhone 11', 'model': 'A2111', 'storage': '64GB', 'color': 'Red', 'price': 7500},
            {'name': 'iPhone 11', 'model': 'A2111', 'storage': '64GB', 'color': 'Purple', 'price': 7500},
            {'name': 'iPhone 11', 'model': 'A2111', 'storage': '64GB', 'color': 'Green', 'price': 7500},
            {'name': 'iPhone 11', 'model': 'A2111', 'storage': '64GB', 'color': 'Yellow', 'price': 7500},
            {'name': 'iPhone 11', 'model': 'A2111', 'storage': '128GB', 'color': 'Black', 'price': 8500},
            {'name': 'iPhone 11', 'model': 'A2111', 'storage': '128GB', 'color': 'White', 'price': 8500},
            {'name': 'iPhone 11', 'model': 'A2111', 'storage': '128GB', 'color': 'Red', 'price': 8500},
            {'name': 'iPhone 11', 'model': 'A2111', 'storage': '128GB', 'color': 'Purple', 'price': 8500},
            {'name': 'iPhone 11', 'model': 'A2111', 'storage': '128GB', 'color': 'Green', 'price': 8500},
            {'name': 'iPhone 11', 'model': 'A2111', 'storage': '128GB', 'color': 'Yellow', 'price': 8500},
            
            {'name': 'iPhone 11 Pro', 'model': 'A2215', 'storage': '64GB', 'color': 'Graphite', 'price': 10500},
            {'name': 'iPhone 11 Pro', 'model': 'A2215', 'storage': '64GB', 'color': 'Gold', 'price': 10500},
            {'name': 'iPhone 11 Pro', 'model': 'A2215', 'storage': '64GB', 'color': 'Silver', 'price': 10500},
            {'name': 'iPhone 11 Pro', 'model': 'A2215', 'storage': '256GB', 'color': 'Graphite', 'price': 12500},
            {'name': 'iPhone 11 Pro', 'model': 'A2215', 'storage': '256GB', 'color': 'Gold', 'price': 12500},
            {'name': 'iPhone 11 Pro', 'model': 'A2215', 'storage': '256GB', 'color': 'Silver', 'price': 12500},
            
            {'name': 'iPhone 11 Pro Max', 'model': 'A2218', 'storage': '64GB', 'color': 'Graphite', 'price': 11999},
            {'name': 'iPhone 11 Pro Max', 'model': 'A2218', 'storage': '64GB', 'color': 'Gold', 'price': 11999},
            {'name': 'iPhone 11 Pro Max', 'model': 'A2218', 'storage': '64GB', 'color': 'Silver', 'price': 11999},
            {'name': 'iPhone 11 Pro Max', 'model': 'A2218', 'storage': '256GB', 'color': 'Graphite', 'price': 13999},
            {'name': 'iPhone 11 Pro Max', 'model': 'A2218', 'storage': '256GB', 'color': 'Gold', 'price': 13999},
            {'name': 'iPhone 11 Pro Max', 'model': 'A2218', 'storage': '256GB', 'color': 'Silver', 'price': 13999},
        ]

        # iPhone 12 Series
        iphone_12_models = [
            {'name': 'iPhone 12', 'model': 'A2403', 'storage': '64GB', 'color': 'Blue', 'price': 10500},
            {'name': 'iPhone 12', 'model': 'A2403', 'storage': '64GB', 'color': 'Black', 'price': 10500},
            {'name': 'iPhone 12', 'model': 'A2403', 'storage': '64GB', 'color': 'White', 'price': 10500},
            {'name': 'iPhone 12', 'model': 'A2403', 'storage': '64GB', 'color': 'Green', 'price': 10500},
            {'name': 'iPhone 12', 'model': 'A2403', 'storage': '64GB', 'color': 'Purple', 'price': 10500},
            {'name': 'iPhone 12', 'model': 'A2403', 'storage': '64GB', 'color': 'Red', 'price': 10500},
            {'name': 'iPhone 12', 'model': 'A2403', 'storage': '128GB', 'color': 'Blue', 'price': 11999},
            {'name': 'iPhone 12', 'model': 'A2403', 'storage': '128GB', 'color': 'Black', 'price': 11999},
            {'name': 'iPhone 12', 'model': 'A2403', 'storage': '128GB', 'color': 'White', 'price': 11999},
            {'name': 'iPhone 12', 'model': 'A2403', 'storage': '128GB', 'color': 'Green', 'price': 11999},
            {'name': 'iPhone 12', 'model': 'A2403', 'storage': '128GB', 'color': 'Purple', 'price': 11999},
            {'name': 'iPhone 12', 'model': 'A2403', 'storage': '128GB', 'color': 'Red', 'price': 11999},
            
            {'name': 'iPhone 12 Pro', 'model': 'A2406', 'storage': '128GB', 'color': 'Graphite', 'price': 14999},
            {'name': 'iPhone 12 Pro', 'model': 'A2406', 'storage': '128GB', 'color': 'Gold', 'price': 14999},
            {'name': 'iPhone 12 Pro', 'model': 'A2406', 'storage': '128GB', 'color': 'Silver', 'price': 14999},
            {'name': 'iPhone 12 Pro', 'model': 'A2406', 'storage': '128GB', 'color': 'Pacific Blue', 'price': 14999},
            {'name': 'iPhone 12 Pro', 'model': 'A2406', 'storage': '256GB', 'color': 'Graphite', 'price': 16999},
            {'name': 'iPhone 12 Pro', 'model': 'A2406', 'storage': '256GB', 'color': 'Gold', 'price': 16999},
            {'name': 'iPhone 12 Pro', 'model': 'A2406', 'storage': '256GB', 'color': 'Silver', 'price': 16999},
            {'name': 'iPhone 12 Pro', 'model': 'A2406', 'storage': '256GB', 'color': 'Pacific Blue', 'price': 16999},
            
            {'name': 'iPhone 12 Pro Max', 'model': 'A2407', 'storage': '128GB', 'color': 'Graphite', 'price': 17999},
            {'name': 'iPhone 12 Pro Max', 'model': 'A2407', 'storage': '128GB', 'color': 'Gold', 'price': 17999},
            {'name': 'iPhone 12 Pro Max', 'model': 'A2407', 'storage': '128GB', 'color': 'Silver', 'price': 17999},
            {'name': 'iPhone 12 Pro Max', 'model': 'A2407', 'storage': '128GB', 'color': 'Pacific Blue', 'price': 17999},
            {'name': 'iPhone 12 Pro Max', 'model': 'A2407', 'storage': '256GB', 'color': 'Graphite', 'price': 19999},
            {'name': 'iPhone 12 Pro Max', 'model': 'A2407', 'storage': '256GB', 'color': 'Gold', 'price': 19999},
            {'name': 'iPhone 12 Pro Max', 'model': 'A2407', 'storage': '256GB', 'color': 'Silver', 'price': 19999},
            {'name': 'iPhone 12 Pro Max', 'model': 'A2407', 'storage': '256GB', 'color': 'Pacific Blue', 'price': 19999},
        ]

        # iPhone 13 Series
        iphone_13_models = [
            {'name': 'iPhone 13', 'model': 'A2482', 'storage': '128GB', 'color': 'Pink', 'price': 13499},
            {'name': 'iPhone 13', 'model': 'A2482', 'storage': '128GB', 'color': 'Blue', 'price': 13499},
            {'name': 'iPhone 13', 'model': 'A2482', 'storage': '128GB', 'color': 'Midnight', 'price': 13499},
            {'name': 'iPhone 13', 'model': 'A2482', 'storage': '128GB', 'color': 'Starlight', 'price': 13499},
            {'name': 'iPhone 13', 'model': 'A2482', 'storage': '128GB', 'color': 'Green', 'price': 13499},
            {'name': 'iPhone 13', 'model': 'A2482', 'storage': '128GB', 'color': 'Red', 'price': 13499},
            {'name': 'iPhone 13', 'model': 'A2482', 'storage': '256GB', 'color': 'Pink', 'price': 15999},
            {'name': 'iPhone 13', 'model': 'A2482', 'storage': '256GB', 'color': 'Blue', 'price': 15999},
            {'name': 'iPhone 13', 'model': 'A2482', 'storage': '256GB', 'color': 'Midnight', 'price': 15999},
            {'name': 'iPhone 13', 'model': 'A2482', 'storage': '256GB', 'color': 'Starlight', 'price': 15999},
            {'name': 'iPhone 13', 'model': 'A2482', 'storage': '256GB', 'color': 'Green', 'price': 15999},
            {'name': 'iPhone 13', 'model': 'A2482', 'storage': '256GB', 'color': 'Red', 'price': 15999},
            
            {'name': 'iPhone 13 Pro', 'model': 'A2483', 'storage': '128GB', 'color': 'Graphite', 'price': 18999},
            {'name': 'iPhone 13 Pro', 'model': 'A2483', 'storage': '128GB', 'color': 'Sierra Blue', 'price': 18999},
            {'name': 'iPhone 13 Pro', 'model': 'A2483', 'storage': '128GB', 'color': 'Gold', 'price': 18999},
            {'name': 'iPhone 13 Pro', 'model': 'A2483', 'storage': '128GB', 'color': 'Silver', 'price': 18999},
            {'name': 'iPhone 13 Pro', 'model': 'A2483', 'storage': '256GB', 'color': 'Graphite', 'price': 20999},
            {'name': 'iPhone 13 Pro', 'model': 'A2483', 'storage': '256GB', 'color': 'Sierra Blue', 'price': 20999},
            {'name': 'iPhone 13 Pro', 'model': 'A2483', 'storage': '256GB', 'color': 'Gold', 'price': 20999},
            {'name': 'iPhone 13 Pro', 'model': 'A2483', 'storage': '256GB', 'color': 'Silver', 'price': 20999},
            
            {'name': 'iPhone 13 Pro Max', 'model': 'A2484', 'storage': '128GB', 'color': 'Graphite', 'price': 21499},
            {'name': 'iPhone 13 Pro Max', 'model': 'A2484', 'storage': '128GB', 'color': 'Sierra Blue', 'price': 21499},
            {'name': 'iPhone 13 Pro Max', 'model': 'A2484', 'storage': '128GB', 'color': 'Gold', 'price': 21499},
            {'name': 'iPhone 13 Pro Max', 'model': 'A2484', 'storage': '128GB', 'color': 'Silver', 'price': 21499},
            {'name': 'iPhone 13 Pro Max', 'model': 'A2484', 'storage': '256GB', 'color': 'Graphite', 'price': 23999},
            {'name': 'iPhone 13 Pro Max', 'model': 'A2484', 'storage': '256GB', 'color': 'Sierra Blue', 'price': 23999},
            {'name': 'iPhone 13 Pro Max', 'model': 'A2484', 'storage': '256GB', 'color': 'Gold', 'price': 23999},
            {'name': 'iPhone 13 Pro Max', 'model': 'A2484', 'storage': '256GB', 'color': 'Silver', 'price': 23999},
        ]

        # iPhone 14 Series
        iphone_14_models = [
            {'name': 'iPhone 14', 'model': 'A2649', 'storage': '128GB', 'color': 'Blue', 'price': 14999},
            {'name': 'iPhone 14', 'model': 'A2649', 'storage': '128GB', 'color': 'Purple', 'price': 14999},
            {'name': 'iPhone 14', 'model': 'A2649', 'storage': '128GB', 'color': 'Yellow', 'price': 14999},
            {'name': 'iPhone 14', 'model': 'A2649', 'storage': '128GB', 'color': 'Red', 'price': 14999},
            {'name': 'iPhone 14', 'model': 'A2649', 'storage': '128GB', 'color': 'Starlight', 'price': 14999},
            {'name': 'iPhone 14', 'model': 'A2649', 'storage': '128GB', 'color': 'Midnight', 'price': 14999},
            {'name': 'iPhone 14', 'model': 'A2649', 'storage': '256GB', 'color': 'Blue', 'price': 17499},
            {'name': 'iPhone 14', 'model': 'A2649', 'storage': '256GB', 'color': 'Purple', 'price': 17499},
            {'name': 'iPhone 14', 'model': 'A2649', 'storage': '256GB', 'color': 'Yellow', 'price': 17499},
            {'name': 'iPhone 14', 'model': 'A2649', 'storage': '256GB', 'color': 'Red', 'price': 17499},
            {'name': 'iPhone 14', 'model': 'A2649', 'storage': '256GB', 'color': 'Starlight', 'price': 17499},
            {'name': 'iPhone 14', 'model': 'A2649', 'storage': '256GB', 'color': 'Midnight', 'price': 17499},
            
            {'name': 'iPhone 14 Pro', 'model': 'A2650', 'storage': '128GB', 'color': 'Deep Purple', 'price': 21999},
            {'name': 'iPhone 14 Pro', 'model': 'A2650', 'storage': '128GB', 'color': 'Gold', 'price': 21999},
            {'name': 'iPhone 14 Pro', 'model': 'A2650', 'storage': '128GB', 'color': 'Silver', 'price': 21999},
            {'name': 'iPhone 14 Pro', 'model': 'A2650', 'storage': '128GB', 'color': 'Space Black', 'price': 21999},
            {'name': 'iPhone 14 Pro', 'model': 'A2650', 'storage': '256GB', 'color': 'Deep Purple', 'price': 24999},
            {'name': 'iPhone 14 Pro', 'model': 'A2650', 'storage': '256GB', 'color': 'Gold', 'price': 24999},
            {'name': 'iPhone 14 Pro', 'model': 'A2650', 'storage': '256GB', 'color': 'Silver', 'price': 24999},
            {'name': 'iPhone 14 Pro', 'model': 'A2650', 'storage': '256GB', 'color': 'Space Black', 'price': 24999},
            
            {'name': 'iPhone 14 Pro Max', 'model': 'A2651', 'storage': '128GB', 'color': 'Deep Purple', 'price': 25999},
            {'name': 'iPhone 14 Pro Max', 'model': 'A2651', 'storage': '128GB', 'color': 'Gold', 'price': 25999},
            {'name': 'iPhone 14 Pro Max', 'model': 'A2651', 'storage': '128GB', 'color': 'Silver', 'price': 25999},
            {'name': 'iPhone 14 Pro Max', 'model': 'A2651', 'storage': '128GB', 'color': 'Space Black', 'price': 25999},
            {'name': 'iPhone 14 Pro Max', 'model': 'A2651', 'storage': '256GB', 'color': 'Deep Purple', 'price': 28999},
            {'name': 'iPhone 14 Pro Max', 'model': 'A2651', 'storage': '256GB', 'color': 'Gold', 'price': 28999},
            {'name': 'iPhone 14 Pro Max', 'model': 'A2651', 'storage': '256GB', 'color': 'Silver', 'price': 28999},
            {'name': 'iPhone 14 Pro Max', 'model': 'A2651', 'storage': '256GB', 'color': 'Space Black', 'price': 28999},
        ]

        # iPhone 15 Series
        iphone_15_models = [
            {'name': 'iPhone 15', 'model': 'A2849', 'storage': '128GB', 'color': 'Pink', 'price': 16999},
            {'name': 'iPhone 15', 'model': 'A2849', 'storage': '128GB', 'color': 'Yellow', 'price': 16999},
            {'name': 'iPhone 15', 'model': 'A2849', 'storage': '128GB', 'color': 'Green', 'price': 16999},
            {'name': 'iPhone 15', 'model': 'A2849', 'storage': '128GB', 'color': 'Blue', 'price': 16999},
            {'name': 'iPhone 15', 'model': 'A2849', 'storage': '128GB', 'color': 'Black', 'price': 16999},
            {'name': 'iPhone 15', 'model': 'A2849', 'storage': '256GB', 'color': 'Pink', 'price': 19499},
            {'name': 'iPhone 15', 'model': 'A2849', 'storage': '256GB', 'color': 'Yellow', 'price': 19499},
            {'name': 'iPhone 15', 'model': 'A2849', 'storage': '256GB', 'color': 'Green', 'price': 19499},
            {'name': 'iPhone 15', 'model': 'A2849', 'storage': '256GB', 'color': 'Blue', 'price': 19499},
            {'name': 'iPhone 15', 'model': 'A2849', 'storage': '256GB', 'color': 'Black', 'price': 19499},
            
            {'name': 'iPhone 15 Pro', 'model': 'A2850', 'storage': '128GB', 'color': 'Blue Titanium', 'price': 25499},
            {'name': 'iPhone 15 Pro', 'model': 'A2850', 'storage': '128GB', 'color': 'White Titanium', 'price': 25499},
            {'name': 'iPhone 15 Pro', 'model': 'A2850', 'storage': '128GB', 'color': 'Natural Titanium', 'price': 25499},
            {'name': 'iPhone 15 Pro', 'model': 'A2850', 'storage': '128GB', 'color': 'Black Titanium', 'price': 25499},
            {'name': 'iPhone 15 Pro', 'model': 'A2850', 'storage': '256GB', 'color': 'Blue Titanium', 'price': 27999},
            {'name': 'iPhone 15 Pro', 'model': 'A2850', 'storage': '256GB', 'color': 'White Titanium', 'price': 27999},
            {'name': 'iPhone 15 Pro', 'model': 'A2850', 'storage': '256GB', 'color': 'Natural Titanium', 'price': 27999},
            {'name': 'iPhone 15 Pro', 'model': 'A2850', 'storage': '256GB', 'color': 'Black Titanium', 'price': 27999},
            
            {'name': 'iPhone 15 Pro Max', 'model': 'A2851', 'storage': '256GB', 'color': 'Blue Titanium', 'price': 30999},
            {'name': 'iPhone 15 Pro Max', 'model': 'A2851', 'storage': '256GB', 'color': 'White Titanium', 'price': 30999},
            {'name': 'iPhone 15 Pro Max', 'model': 'A2851', 'storage': '256GB', 'color': 'Natural Titanium', 'price': 30999},
            {'name': 'iPhone 15 Pro Max', 'model': 'A2851', 'storage': '256GB', 'color': 'Black Titanium', 'price': 30999},
            {'name': 'iPhone 15 Pro Max', 'model': 'A2851', 'storage': '512GB', 'color': 'Blue Titanium', 'price': 34999},
            {'name': 'iPhone 15 Pro Max', 'model': 'A2851', 'storage': '512GB', 'color': 'White Titanium', 'price': 34999},
            {'name': 'iPhone 15 Pro Max', 'model': 'A2851', 'storage': '512GB', 'color': 'Natural Titanium', 'price': 34999},
            {'name': 'iPhone 15 Pro Max', 'model': 'A2851', 'storage': '512GB', 'color': 'Black Titanium', 'price': 34999},
        ]

        # iPhone 16 Pro Max (Latest Model)
        iphone_16_models = [
            {'name': 'iPhone 16 Pro Max', 'model': 'A2852', 'storage': '256GB', 'color': 'Black Titanium', 'price': 30499},
            {'name': 'iPhone 16 Pro Max', 'model': 'A2852', 'storage': '256GB', 'color': 'White Titanium', 'price': 30499},
            {'name': 'iPhone 16 Pro Max', 'model': 'A2852', 'storage': '256GB', 'color': 'Natural Titanium', 'price': 30499},
            {'name': 'iPhone 16 Pro Max', 'model': 'A2852', 'storage': '256GB', 'color': 'Desert Titanium', 'price': 30999},
            {'name': 'iPhone 16 Pro Max', 'model': 'A2852', 'storage': '512GB', 'color': 'Black Titanium', 'price': 35999},
            {'name': 'iPhone 16 Pro Max', 'model': 'A2852', 'storage': '512GB', 'color': 'White Titanium', 'price': 35999},
            {'name': 'iPhone 16 Pro Max', 'model': 'A2852', 'storage': '512GB', 'color': 'Natural Titanium', 'price': 35999},
            {'name': 'iPhone 16 Pro Max', 'model': 'A2852', 'storage': '512GB', 'color': 'Desert Titanium', 'price': 36499},
            {'name': 'iPhone 16 Pro Max', 'model': 'A2852', 'storage': '1TB', 'color': 'Black Titanium', 'price': 41999},
            {'name': 'iPhone 16 Pro Max', 'model': 'A2852', 'storage': '1TB', 'color': 'White Titanium', 'price': 41999},
            {'name': 'iPhone 16 Pro Max', 'model': 'A2852', 'storage': '1TB', 'color': 'Natural Titanium', 'price': 41999},
            {'name': 'iPhone 16 Pro Max', 'model': 'A2852', 'storage': '1TB', 'color': 'Desert Titanium', 'price': 42499},
        ]

        # Combine all models
        all_models = (iphone_11_models + iphone_12_models + iphone_13_models + 
                     iphone_14_models + iphone_15_models + iphone_16_models)

        # Create phones in database
        phones_created = 0
        for model_data in all_models:
            phone = Phone.objects.create(
                name=model_data['name'],
                model=model_data['model'],
                storage=model_data['storage'],
                color=model_data['color'],
                price=model_data['price'],
                is_available=True
            )
            phones_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {phones_created} iPhone models with realistic South African prices in ZAR!'
            )
        )
        
        # Display summary
        self.stdout.write('\n📱 iPhone Price Summary:')
        self.stdout.write('=' * 50)
        
        series_summary = {}
        for model_data in all_models:
            series = model_data['name'].split()[1]  # Extract series (11, 12, 13, etc.)
            if series not in series_summary:
                series_summary[series] = {'count': 0, 'min_price': float('inf'), 'max_price': 0}
            
            series_summary[series]['count'] += 1
            price = model_data['price']
            series_summary[series]['min_price'] = min(series_summary[series]['min_price'], price)
            series_summary[series]['max_price'] = max(series_summary[series]['max_price'], price)
        
        for series in sorted(series_summary.keys(), key=lambda x: int(x) if x.isdigit() else 0):
            data = series_summary[series]
            self.stdout.write(
                f'iPhone {series}: {data["count"]} models - R{data["min_price"]:,} to R{data["max_price"]:,}'
            ) 