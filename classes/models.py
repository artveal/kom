from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import datetime

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, is_admin=False, is_active=True):
        if not username:
            raise ValueError("Users must have an username")
        if not email:
            raise ValueError("Users must have an email")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(email= self.normalize_email(email))
        user_obj.username = username
        user_obj.set_password(password)
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, username, email, password):
        user_obj = self.create_user(username, email, password, is_admin=True, is_active=True)
        return user_obj

class User(AbstractBaseUser):
    ''' Game users '''
    username = models.CharField(max_length=40, unique=True)
    email    = models.EmailField(max_length=254)
    active   = models.BooleanField(default=True)
    admin    = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    @ property
    def is_active(self):
        return self.active

    @ property
    def is_staff(self):
        return self.admin

    @ property
    def is_admin(self):
        return self.admin

class News(models.Model):
    ''' Official news '''
    title           = models.CharField(max_length=20)
    abstract        = models.TextField(max_length=400, blank=True)
    content         = models.TextField(max_length=4000, blank=True)
    pub_date        = models.DateTimeField(default=datetime.datetime.now)
    author          = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "News"

    def __str__(self):
        return self.title

class Nation(models.Model):
    ''' Nations of game'''
    name            = models.CharField(max_length=40)
    abbr            = models.CharField(max_length=4, unique=True)
    association     = models.CharField(max_length=15, blank=True)
    path            = models.TextField(blank=True)
    # flag
    
    def __str__(self):
        return self.name

'''
class Notification(models.Model):
    title           = models.CharField(max_length=40)
    content         = models.TextField(max_length=200)
    url
    receiver        = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="sender", blank=True, null=True)
    date            = models.DateTimeField(default=datetime.datetime.now)
'''

class Season(models.Model):
    ''' This model stores all season info'''
    name            = models.CharField(max_length=20)
    start_date      = models.DateField(auto_now=False)
    end_date        = models.DateField(auto_now=False)

    # transfer markets windows
    transfer_market_1_start      = models.DateField(auto_now=False)
    transfer_market_1_end        = models.DateField(auto_now=False)
    transfer_market_2_start      = models.DateField(auto_now=False)
    transfer_market_2_end        = models.DateField(auto_now=False)

    # weather settings. Types will be distributed equally of season length
    weather_type_start           = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(4), MinValueValidator(1)])
    weather_type_end             = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(4), MinValueValidator(1)])

    def __str__(self):
        return self.name

class Weather(models.Model):
    name                    = models.CharField(max_length=40)
    season_1_temperature    = models.IntegerField(default=25, help_text="in Celsius degrees")
    season_1_rain           = models.IntegerField(default=25, help_text="percent. Chances to have rain or snow", validators=[MaxValueValidator(0), MinValueValidator(100)])
    season_2_temperature    = models.IntegerField(default=25, help_text="in Celsius degrees")
    season_2_rain           = models.IntegerField(default=25, help_text="percent. Chances to have rain or snow", validators=[MaxValueValidator(0), MinValueValidator(100)])
    season_3_temperature    = models.IntegerField(default=25, help_text="in Celsius degrees")
    season_3_rain           = models.IntegerField(default=25, help_text="percent. Chances to have rain or snow", validators=[MaxValueValidator(0), MinValueValidator(100)])
    season_4_temperature    = models.IntegerField(default=25, help_text="in Celsius degrees")
    season_4_rain           = models.IntegerField(default=25, help_text="percent. Chances to have rain or snow", validators=[MaxValueValidator(0), MinValueValidator(100)])
    
    def __str__(self):
        self.name

class City(models.Model):
    name            = models.CharField(max_length=40)
    nation          = models.ForeignKey(Nation, on_delete=models.SET_NULL, null=True)
    latitude        = models.FloatField(default=0, validators=[MaxValueValidator(90), MinValueValidator(-90)])
    longitude       = models.FloatField(default=0, validators=[MaxValueValidator(180), MinValueValidator(-180)])
    weather         = models.ForeignKey(Weather, on_delete=models.SET_NULL, null=True, default=None)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        self.name + " (" + self.nation + ")"

class Stadium(models.Model):
    name            = models.CharField(max_length=40)
    city            = models.CharField(max_length=20)
    capacity        = models.CharField(max_length=20)
    maintenance     = models.IntegerField(default=5, validators=[MaxValueValidator(0), MinValueValidator(5)])
    services        = models.IntegerField(default=5, validators=[MaxValueValidator(0), MinValueValidator(5)])

    def __str__(self):
        return self.name

class Competition(models.Model):
    ''' Used to set generic rules for every season of this competition'''
    name                = models.CharField(max_length=40)           # Competiton name
    tier                = models.PositiveIntegerField(default=1)    # Competiton tier (1 for first division and so on)
    association         = models.CharField(max_length=25)           # Organizer entity. Will be used to sort competitions
    # logo              =
    
    # Competition type. Will be used to determine how sanctions are considered.
    # Competitions can be local (e.g. Premier League or FA Cup), international (e.g. UEFA Champions League) or national team (e.g. FIFA World Cup)
    LOCAL, INTERNATIONAL, NATIONAL_TEAMS= ('local', 'international', 'national_teams')
    COMPETITION_TYPE = [(LOCAL, 'Local'), (INTERNATIONAL, 'International'), (NATIONAL_TEAMS, 'National teams')]
    competition_type    = models.CharField(max_length=15, choices=COMPETITION_TYPE, default=LOCAL)

    active              = models.BooleanField(default=True)         # Set False if it is no longer disputed. Used to automaticly generate seasons.

    def __str__(self):
        return self.name

class CompetitionRoundAbstract(models.Model):
    ''' Used to set generic rules for every round of this competition and its season instances '''
    name            = models.CharField(max_length=40)                           # Round name
     
    # Round format. Will be used to determine if round is organized by eliminatories (cup) or matchdays and league table (table)
    ROUND_FORMAT = [('league', 'League'), ('cup', 'Cup')]
    round_format = models.CharField(max_length=15, choices=ROUND_FORMAT, default='league')

    # Number of rounds. In leagues, every team will play against each qualified team x times. In cups, player will play againt its opponent x times.
    number_of_rounds = models.PositiveIntegerField(default=2)

    # Tiebreak rule for eliminatories.
    TIEBREAK = [
        ('et_away_goals', 'Use away goals rule (if # of rounds > 1). If tied, play extra time and penalty shootout'),
        ('et', 'Play extra time and penalty shootout directly'),
        ('penalties', "Play penalty shootout directly")
    ]
    tiebreak_rule   = models.CharField(max_length=15, choices=TIEBREAK, default='et_away_goals', help_text="Only for cup rounds")

    # Rule to determine positions in league tables. First 
    TABLE_TIEBREAK = [
        ('global', 'Goal difference > Scored goals (global table)'),
        ('local', 'Results between tied teams will be used to tiebreak. If still tied, use global tiebreak')
    ]
    table_tiebreak  = models.CharField(max_length=15, choices=TABLE_TIEBREAK, default='local', help_text="Only for leagues")

    final_round     = models.BooleanField(default=False, help_text="If enabled, the winner will be recognized as champion in its career section")

    class Meta:
        abstract = True

class CompetitionRound(CompetitionRoundAbstract):
    ''' Used to set generic rules for every round of this competition'''
    competition     = models.ForeignKey(Competition, on_delete=models.CASCADE)  # Competition in which the round is played    

    def __str__(self):
        return self.name + " (" + self.competition.__str__() + ")"

class QualifyingRelation(models.Model):
    ''' Join table to specify how advancing to next rounds/leagues is set. Also sets economic reward. ALWAYS SEARCH CLOSEST NON STARTED ROUND'''
    from_round          = models.ForeignKey(CompetitionRound, on_delete=models.SET_NULL, related_name="from_round", blank=True, null=True) 
    to_round            = models.ForeignKey(CompetitionRound, on_delete=models.SET_NULL, related_name="to_round", blank=True, null=True)
    position            = models.PositiveIntegerField(default=1) # For cup rounds 1=Winner, 2=Losser
    economic_reward     = models.IntegerField(default=0)

    def __str__(self):
        return "from [" + str(self.position) + "] " + self.from_round + " to " + self.to_round

class CompetitionSeason(models.Model):
    ''' Instance of competition for specific season'''
    competition     = models.ForeignKey(Competition, on_delete=models.CASCADE)
    season          = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return self.competition.__str__() + " (" + self.season.__str__() + ")"

class CompetitionSeasonRound(CompetitionRoundAbstract):
    ''' Season specific rules for round of competition.'''
    competition     = models.ForeignKey(CompetitionSeason, on_delete=models.CASCADE)  # Competition in which the round is played

    def __str__(self):
        return self.name + " (" + self.competition.__str__() + ")"

class Sponsor(models.Model):
    name            = models.CharField(max_length=40)
    #logo

    def __str__(self):
        return self.name

class Team(models.Model):
    name            = models.CharField(max_length=40)
    abbr            = models.CharField(max_length=4, unique=True)
    manager         = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="User", blank=True,  null=True)
    stadium         = models.ForeignKey(Stadium, on_delete=models.SET_NULL, verbose_name="Stadium", blank=True,  null=True)
    sponsor         = models.ForeignKey(Sponsor, on_delete=models.SET_NULL, verbose_name="Sponsor", blank=True,  null=True)
    #logo            = 
    shirt1_style    = models.CharField(max_length=20, default="style1", verbose_name="Home shirt style")
    shirt1_color1   = models.CharField(max_length=20, default="#ffffff", verbose_name="Home shirt main color")
    shirt1_color2   = models.CharField(max_length=20, default="#000000", verbose_name="Home shirt details color")
    shirt2_style    = models.CharField(max_length=20, default="style1", verbose_name="Away shirt style")
    shirt2_color1   = models.CharField(max_length=20, default="#000000", verbose_name="Away shirt main color")
    shirt2_color2   = models.CharField(max_length=20, default="#ffffff", verbose_name="Away shirt details color")

    budget          = models.IntegerField(default=0)
    elo_points      = models.IntegerField(default=0)

    national_team   = models.ForeignKey(Nation, on_delete=models.SET_NULL, help_text="Leave blank if team is not a national team", verbose_name="National team", blank=True, null=True)
    playable        = models.BooleanField(default=True)
    active          = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TeamPerformance(models.Model):
    team                = models.ForeignKey(Team, on_delete=models.CASCADE)
    competition         = models.ForeignKey(CompetitionSeasonRound, on_delete=models.CASCADE)
    points              = models.IntegerField(default=0)
    scored_goals        = models.IntegerField(default=0)
    received_goals      = models.IntegerField(default=0)
    wins                = models.IntegerField(default=0)
    draws               = models.IntegerField(default=0)
    losses              = models.IntegerField(default=0)

    def __str__(self):
        return self.team.name + " on " + self.competition.__str__()

    def goal_difference(self):
        return self.scored_goals - self.received_goals

class Player(models.Model):
    objects = models.Manager()
    full_name       = models.CharField(max_length=100)
    short_name      = models.CharField(max_length=40)
    age             = models.PositiveIntegerField()

    # nationality and nation team
    nationality     = models.ForeignKey(Nation, on_delete=models.SET_NULL, verbose_name="Nationality", null=True)
    n_shirt_number  = models.PositiveIntegerField(null=True, blank=True, validators=[MaxValueValidator(99), MinValueValidator(1)], verbose_name="National team shirt number") # this will also indicate if player is capped for national team
    #picture         =

    # position
    POSITIONS_CHOICES = [
        ("GK", "Goalkeeper"),           # goalkeeper
        ("CD", "Centre Defender"),      # defender
        ("LD", "Left Defender"),        # defender
        ("RD", "Right Defender"),       # defender
        ("LW", "Left Wingback"),        # defender
        ("RW", "Right Wingback"),       # defender
        ("DM", "Defensive Midfielder"), # midfielder
        ("CM", "Centre Midfielder"),    # midfielder
        ("LM", "Left Midfielder"),      # midfielder
        ("RM", "Right Midfielder"),     # midfielder
        ("OM", "Offensive Midfielder"), # midfielder
        ("CF", "Centre Forward"),       # forward
        ("LF", "Left Forward"),         # forward
        ("RF", "Right Forward"),        # forward
    ]
    position1        = models.CharField(max_length=2, choices=POSITIONS_CHOICES, blank=False, default="GK")
    position2        = models.CharField(max_length=2, choices=POSITIONS_CHOICES, blank=True, default="")
    position3        = models.CharField(max_length=2, choices=POSITIONS_CHOICES, blank=True, default="")
    position4        = models.CharField(max_length=2, choices=POSITIONS_CHOICES, blank=True, default="")

    # skills
    defending       = models.FloatField(validators=[MaxValueValidator(100), MinValueValidator(1)], default=100)
    passing         = models.FloatField(validators=[MaxValueValidator(100), MinValueValidator(1)], default=100)
    shooting        = models.FloatField(validators=[MaxValueValidator(100), MinValueValidator(1)], default=100)
    dribbling       = models.FloatField(validators=[MaxValueValidator(100), MinValueValidator(1)], default=100)
    stamina         = models.FloatField(validators=[MaxValueValidator(100), MinValueValidator(1)], default=100)
    pace            = models.FloatField(validators=[MaxValueValidator(100), MinValueValidator(1)], default=100)
    strength        = models.FloatField(validators=[MaxValueValidator(100), MinValueValidator(1)], default=100)
    potential       = models.FloatField(validators=[MaxValueValidator(100), MinValueValidator(1)])

    # status
    fitness         = models.PositiveIntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)], default=100)
    injury_time     = models.PositiveIntegerField(default=0)
    domestic_susp   = models.PositiveIntegerField(default=0, verbose_name="Domestic competitions suspension") # domestic competitions (leagues and cups) suspension matches
    int_susp        = models.PositiveIntegerField(default=0, verbose_name="Int. club competitions suspension") # international club competitions suspension matches
    nt_susp         = models.PositiveIntegerField(default=0, verbose_name="National team suspension") # national team competitions suspension matches
    active          = models.BooleanField(default=True)
    yellow_cards_d  = models.PositiveIntegerField(default=0, verbose_name="Domestic competitions yellow cards")
    yellow_cards_i  = models.PositiveIntegerField(default=0, verbose_name="Int. club competitions yellow cards")
    yellow_cards_n  = models.PositiveIntegerField(default=0, verbose_name="National team yellow cards")
    
    # transfer and loan status
    TRANSFERABLE    = 'Trn'
    NON_TRANSFERABLE= 'NTrn'
    AVAILABLE_LOAN  = 'Loa'
    NON_AV_LOAN     = 'NLoa'
    NON_SET         = 'unset'
    
    TRANSFER_CHOICES = [
        (TRANSFERABLE, 'Transferable'),
        (NON_TRANSFERABLE, 'Non transferable'),
        (NON_SET, 'Non set'),
    ]

    LOAN_CHOICES = [
        (AVAILABLE_LOAN, 'Available loan'),
        (NON_AV_LOAN, 'Non available loan'),
        (NON_SET, 'Non set'),
    ]

    transfer_status = models.CharField(max_length=5, choices=TRANSFER_CHOICES, default=NON_SET)
    loan_status     = models.CharField(max_length=5, choices=LOAN_CHOICES, default=NON_SET)

    # team contract
    team            = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name="team", verbose_name="Contract team",  blank=True, null=True)
    t_shirt_number  = models.PositiveIntegerField(null=True, blank=True, validators=[MaxValueValidator(99), MinValueValidator(1)], verbose_name="Team shirt number")
    salary          = models.PositiveIntegerField(default=1)
    contract_length = models.IntegerField(default=0)
    youth_team      = models.BooleanField(default=False)

    loan_by_team    = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name="loan_team", verbose_name="Loaned by",  blank=True, null=True)
    loan_contrib    = models.IntegerField(default=0, verbose_name="Loan contribution", help_text="Paid by current team to loan team")
    loan_length     = models.IntegerField(default=0)

    def __str__(self):
        return self.short_name

    def skills(self):
        return {
            "def": int(self.defending),
            "pas": int(self.passing),
            "sho": int(self.shooting),
            "dri": int(self.dribbling),
            "pac": int(self.pace),
            "phy": int(self.strength),
            "sta": int(self.stamina),
            "pot": int(self.potential),
        }

    def name(self):
        return self.short_name
