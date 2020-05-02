from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin, NestedTabularInline

from .models import *

from .forms import UserAdminCreationForm, UserAdminChangeForm, RoundInlineFormSet

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'admin')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('username', 'email',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

admin.site.register(News)
admin.site.register(Nation)

class SeasonAdmin(admin.ModelAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'start_date', 'end_date', "transfer_market_1_start", "transfer_market_1_end", "transfer_market_2_start", "transfer_market_2_end")
    fieldsets = (
        (None, {'fields': ('name', 'start_date', 'end_date')}),
        ('Transfer Market Window 1', {'fields': ("transfer_market_1_start", "transfer_market_1_end")}),
        ('Transfer Market Window 2', {'fields': ("transfer_market_2_start", "transfer_market_2_end")}),
    )
 

admin.site.register(Season, SeasonAdmin)


admin.site.register(Weather)
admin.site.register(City)
admin.site.register(Stadium)

class RoundsRelationFormInline(NestedTabularInline):
    model = QualifyingRelation
    fk_name = 'from_round'
    fields = ('position', 'to_round','economic_reward')
    extra = 1

class CompetitionRoundsFormInline(NestedStackedInline):
    model = CompetitionRound
    extra = 0
    inlines = [RoundsRelationFormInline]

class CompetitionAdmin(NestedModelAdmin):
    inlines = [CompetitionRoundsFormInline]

admin.site.register(Competition, CompetitionAdmin)

admin.site.register(CompetitionSeason)
admin.site.register(CompetitionSeasonRound)
admin.site.register(Sponsor)
admin.site.register(Team)
admin.site.register(TeamPerformance)

class PlayerAdmin(admin.ModelAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('short_name', 'team')
    fieldsets = (
        ('Player information', {'fields': ('short_name', 'full_name', 'age', "active")}),
        ('National team', {'fields': ('nationality', 'n_shirt_number')}),
        ('Team info', {'fields': ("team", "t_shirt_number", "salary", "contract_length", "youth_team")}),
        ('Loan info', {'fields': ("loan_by_team", "loan_contrib", "loan_length")}),
        ('Position', {'fields': ("position1", "position2", "position3", "position4")}),
        ('Skills', {'fields': ("potential", "defending", "passing", "shooting", "dribbling", "pace", "strength", "stamina")}),
        ('Status', {'fields': ("fitness", "injury_time", "domestic_susp", "int_susp", "nt_susp")}),
        ('Transfer info', {'fields': ("transfer_status", "loan_status")}),
    )

admin.site.register(Player, PlayerAdmin)


# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
