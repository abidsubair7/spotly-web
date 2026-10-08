from django.db import migrations, models
import django.core.validators

class Migration(migrations.Migration):
    dependencies=[('places','0001_initial')]
    operations=[migrations.CreateModel(name='Review',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('rating',models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1),django.core.validators.MaxValueValidator(5)])),('comment',models.TextField(blank=True,max_length=1000)),('created_at',models.DateTimeField(auto_now_add=True)),('place',models.ForeignKey(on_delete=models.deletion.CASCADE,related_name='reviews',to='places.place')),('user',models.ForeignKey(on_delete=models.deletion.CASCADE,related_name='reviews',to='auth.user'))],options={'ordering':['-created_at']}),migrations.AddConstraint(model_name='review',constraint=models.UniqueConstraint(fields=('place','user'),name='unique_place_review'))]
