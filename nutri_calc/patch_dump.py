import json
from bson.objectid import ObjectId

with open('datadump.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

id_map = {}

# Map models migrating to Mongo
mongo_models = ['ingredients.ingredient', 'recipes.recipe', 'recipes.recipeingredient']

for item in data:
    model = item['model']
    if model in mongo_models:
        old_pk = item['pk']
        new_pk = str(ObjectId())
        id_map[(model, old_pk)] = new_pk
        item['pk'] = new_pk

for item in data:
    model = item['model']
    fields = item['fields']
    if model == 'recipes.recipeingredient':
        old_recipe_id = fields.get('recipe')
        if old_recipe_id and ('recipes.recipe', old_recipe_id) in id_map:
            fields['recipe'] = id_map[('recipes.recipe', old_recipe_id)]

with open('datadump_patched.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
