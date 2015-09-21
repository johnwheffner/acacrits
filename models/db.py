db = DAL('sqlite://acacrits.db')

db.define_table(
    'athlete',
    Field('last_name', required=True),
    Field('first_name', required=True),
    Field('additional_names'),
    Field('suffix'),
    Field('gender', length=1, required=True, requires=IS_IN_SET(('m', 'f'))),
    Field('usac_license_numer', 'integer'))
db.athlete.id.readable = False

db.define_table(
    'official',
    Field('last_name', required=True),
    Field('first_name', required=True),
    Field('additional_names'),
    Field('suffix'))
db.official.id.readable = False

db.define_table(
    'season',
    Field('year', 'integer', required=True, unique=True))

db.define_table(
    'race_class',
    Field('description', required=True, unique=True))

db.define_table(
    'race_class_season',
    Field('race_class_id', 'reference race_class'),
    Field('season_id', 'reference season',
          requires=IS_IN_DB(db, db.season.id, '%(year)d')))

db.define_table(
    'race_subclass',
    Field('description', required=True, unique=True))

db.define_table(
    'race_subclass_season',
    Field('race_subclass_id', 'reference race_subclass'),
    Field('race_class_season_id', 'reference race_class_season'))

db.define_table(
    'raceday',
    Field('date', 'date', required=True),
    Field('conditions'),
    Field('temperature_f', 'double'))

db.define_table(
    'racedayofficial',
    Field('raceday_id', 'reference raceday'),
    Field('official_id', 'reference official'))

db.define_table(
    'race',
    Field('date', 'date', required=True),
    Field('class_id', 'reference race_class', required=True,
          requires=IS_IN_DB(db, db.race_class.id, '%(description)s')),
    Field('laps', 'integer'),
    Field('slow_lap_secs', 'double'),
    Field('fast_lap_secs', 'double'),
    Field('average_lap_secs', 'double'))

db.define_table(
    'team',
    Field('name', required=True, unique=True))

db.define_table(
    'athleteteam',
    Field('athlete_id', 'reference athlete'),
    Field('team_id', 'reference team'),
    Field('season_id', 'reference season',
          requires=IS_IN_DB(db, db.season.id, '%(year)d')))

db.define_table(
    'participant',
    Field('athlete_id', 'reference athlete', required=True),
    Field('team_id', 'reference team'),
    Field('race_id', 'reference race', required=True))

db.define_table(
    'result',
    Field('participant_id', 'reference participant', required=True),
    Field('place', 'integer'),
    Field('points', 'double'),
    Field('mar_place', 'integer'),
    Field('point_prime', 'boolean'))

db.define_table(
    'subclassresult',
    Field('participant_id', 'reference participant', required=True),
    Field('subclass_id', 'reference race_subclass', required=True),
    Field('place', 'integer'),
    Field('points', 'double'))

db.define_table(
    'prime',
    Field('participant_id', 'reference participant'),
    Field('description'))