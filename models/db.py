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
    'marshal',
    Field('last_name', required=True),
    Field('first_name', required=True),
    Field('additional_names'),
    Field('suffix'))
db.marshal.id.readable = False

db.define_table(
    'season',
    Field('year', 'integer', required=True, unique=True))

db.define_table(
    'race_class',
    Field('description', required=True, unique=True))

db.define_table(
    'race_subclass',
    Field('description', required=True, unique=True))

db.define_table(
    'race_day',
    Field('date', 'date', required=True),
    Field('conditions'),
    Field('temperature_f', 'double'))

db.define_table(
    'race_day_official',
    Field('race_day_id', 'reference race_day'),
    Field('official_id', 'reference official'))

db.define_table(
    'race',
    Field('date', 'date', required=True),
    Field('class_id', 'reference race_class', required=True,
          requires=IS_IN_DB(db, db.race_class.id, '%(description)s')),
    Field('laps', 'integer'),
    Field('slow_lap_secs', 'double'),
    Field('fast_lap_secs', 'double'),
    Field('average_lap_secs', 'double'),
    Field('starters', 'integer'),
    Field('finish_time_secs', 'double'))

db.define_table(
    'team',
    Field('name', required=True, unique=True))
db.team.id.readable = False

db.define_table(
    'athlete_team',
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
    'race_marshal',
    Field('race_id', 'reference race', required=True),
    Field('marshal_id', 'reference marshal', required=True))

db.define_table(
    'result',
    Field('participant_id', 'reference participant', required=True),
    Field('place', 'integer'),
    Field('points', 'double'),
    Field('mar_place', 'integer'),
    Field('point_prime', 'boolean'))

db.define_table(
    'subclass_result',
    Field('participant_id', 'reference participant', required=True),
    Field('subclass_id', 'reference race_subclass', required=True),
    Field('place', 'integer'),
    Field('points', 'double'))

db.define_table(
    'prime',
    Field('participant_id', 'reference participant'),
    Field('description'))


def load_hard_coded_data():
    def update_table(table, table_data):
        cur_table_data = db().select(table.ALL)
        cur_keys = set()
        for row in cur_table_data:
            cur_keys.add(row.id)
            non_id_vals = {k: v for k, v in row.items() if k != 'id'}
            if row.id in table_data:
                table[row.id] = table_data[row.id]
            else:
                del table[row.id]
        for key, val in table_data.items():
            if not key in cur_keys:
                table.insert(**val)

    CURRENT_SEASON = 2015
    SEASONS_TABLE = {
        i+1: dict(year=year) for i, year in
        enumerate(xrange(1996, CURRENT_SEASON+1))}
    update_table(db.season, SEASONS_TABLE)

    CLASSES = ['A', 'B', 'C', 'Masters 40+/Women', 'Juniors']
    CLASSES_TABLE = {
        i+1: dict(description=description)
        for i, description in enumerate(CLASSES)}
    update_table(db.race_class, CLASSES_TABLE)

    SUBCLASSES = ['Women', 'Juniors']
    SUBCLASSES_TABLE = {
        i+1:dict(description=description)
        for i, description in enumerate(SUBCLASSES)}
    update_table(db.race_subclass, SUBCLASSES_TABLE)

    db.commit()


load_hard_coded_data()
del load_hard_coded_data
