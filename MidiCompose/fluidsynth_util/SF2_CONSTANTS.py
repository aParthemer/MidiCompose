from dataclasses import dataclass
from collections import namedtuple


FLUIDR3_GM_PATH = "/c/Users/Alex/soundfonts/FluidR3_GM.sf2"
FLUIDR3_GM_DICT = {'Yamaha Grand Piano': [0, 0],
                   'Bright Yamaha Grand': [0, 1],
                   'Electric Piano': [0, 2],
                   'Honky Tonk': [0, 3],
                   'Rhodes EP': [0, 4],
                   'Legend EP 2': [0, 5],
                   'Harpsichord': [0, 6],
                   'Clavinet': [0, 7],
                   'Celesta': [0, 8],
                   'Glockenspiel': [0, 9],
                   'Music Box': [0, 10],
                   'Vibraphone': [0, 11],
                   'Marimba': [0, 12],
                   'Xylophone': [0, 13],
                   'Tubular Bells': [0, 14],
                   'Dulcimer': [0, 15],
                   'DrawbarOrgan': [0, 16],
                   'Percussive Organ': [0, 17],
                   'Rock Organ': [0, 18],
                   'Church Organ': [0, 19],
                   'Reed Organ': [0, 20],
                   'Accordian': [0, 21],
                   'Harmonica': [0, 22],
                   'Bandoneon': [0, 23],
                   'Nylon String Guitar': [0, 24],
                   'Steel String Guitar': [0, 25],
                   'Jazz Guitar': [0, 26],
                   'Clean Guitar': [0, 27],
                   'Palm Muted Guitar': [0, 28],
                   'Overdrive Guitar': [0, 29],
                   'Distortion Guitar': [0, 30],
                   'Guitar Harmonics': [0, 31],
                   'Acoustic Bass': [0, 32],
                   'Fingered Bass': [0, 33],
                   'Picked Bass': [0, 34],
                   'Fretless Bass': [0, 35],
                   'Slap Bass': [0, 36],
                   'Pop Bass': [0, 37],
                   'Synth Bass 1': [0, 38],
                   'Synth Bass 2': [0, 39],
                   'Violin': [0, 40],
                   'Viola': [0, 41],
                   'Cello': [0, 42],
                   'Contrabass': [0, 43],
                   'Tremolo': [0, 44],
                   'Pizzicato Section': [0, 45],
                   'Harp': [0, 46],
                   'Timpani': [0, 47],
                   'Strings': [0, 48],
                   'Slow Strings': [0, 49],
                   'Synth Strings 1': [0, 50],
                   'Synth Strings 2': [0, 51],
                   'Ahh Choir': [0, 52],
                   'Ohh Voices': [0, 53],
                   'Synth Voice': [0, 54],
                   'Orchestra Hit': [0, 55],
                   'Trumpet': [0, 56],
                   'Trombone': [0, 57],
                   'Tuba': [0, 58],
                   'Muted Trumpet': [0, 59],
                   'French Horns': [0, 60],
                   'Brass Section': [0, 61],
                   'Synth Brass 1': [0, 62],
                   'Synth Brass 2': [0, 63],
                   'Soprano Sax': [0, 64],
                   'Alto Sax': [0, 65],
                   'Tenor Sax': [0, 66],
                   'Baritone Sax': [0, 67],
                   'Oboe': [0, 68],
                   'English Horn': [0, 69],
                   'Bassoon': [0, 70],
                   'Clarinet': [0, 71],
                   'Piccolo': [0, 72],
                   'Flute': [0, 73],
                   'Recorder': [0, 74],
                   'Pan Flute': [0, 75],
                   'Bottle Chiff': [0, 76],
                   'Shakuhachi': [0, 77],
                   'Whistle': [0, 78],
                   'Ocarina': [0, 79],
                   'Square Lead': [0, 80],
                   'Saw Wave': [0, 81],
                   'Calliope Lead': [0, 82],
                   'Chiffer Lead': [0, 83],
                   'Charang': [0, 84],
                   'Solo Vox': [0, 85],
                   'Fifth Sawtooth Wave': [0, 86],
                   'Bass & Lead': [0, 87],
                   'Fantasia': [0, 88],
                   'Warm Pad': [0, 89],
                   'Polysynth': [0, 90],
                   'Space Voice': [0, 91],
                   'Bowed Glass': [0, 92],
                   'Metal Pad': [0, 93],
                   'Halo Pad': [0, 94],
                   'Sweep Pad': [0, 95],
                   'Ice Rain': [0, 96],
                   'Soundtrack': [0, 97],
                   'Crystal': [0, 98],
                   'Atmosphere': [0, 99],
                   'Brightness': [0, 100],
                   'Goblin': [0, 101],
                   'Echo Drops': [0, 102],
                   'Star Theme': [0, 103],
                   'Sitar': [0, 104],
                   'Banjo': [0, 105],
                   'Shamisen': [0, 106],
                   'Koto': [0, 107],
                   'Kalimba': [0, 108],
                   'BagPipe': [0, 109],
                   'Fiddle': [0, 110],
                   'Shenai': [0, 111],
                   'Tinker Bell': [0, 112],
                   'Agogo': [0, 113],
                   'Steel Drums': [0, 114],
                   'Woodblock': [0, 115],
                   'Taiko Drum': [0, 116],
                   'Melodic Tom': [0, 117],
                   'Synth Drum': [0, 118],
                   'Reverse Cymbal': [0, 119],
                   'Fret Noise': [0, 120],
                   'Breath Noise': [0, 121],
                   'Sea Shore': [0, 122],
                   'Bird Tweet': [0, 123],
                   'Telephone': [0, 124],
                   'Helicopter': [0, 125],
                   'Applause': [0, 126],
                   'Gun Shot': [0, 127],
                   'Detuned EP 1': [8, 4],
                   'Detuned EP 2': [8, 5],
                   'Coupled Harpsichord': [8, 6],
                   'Church Bell': [8, 14],
                   'Detuned Organ 1': [8, 16],
                   'Detuned Organ 2': [8, 17],
                   'Church Organ 2': [8, 19],
                   'Italian Accordion': [8, 21],
                   'Ukulele': [8, 24],
                   '12 String Guitar': [8, 25],
                   'Hawaiian Guitar': [8, 26],
                   'Funk Guitar': [8, 28],
                   'Feedback Guitar': [8, 30],
                   'Guitar Feedback': [8, 31],
                   'Synth Bass 3': [8, 38],
                   'Synth Bass 4': [8, 39],
                   'Slow Violin': [8, 40],
                   'Orchestral Pad': [8, 48],
                   'Synth Strings 3': [8, 50],
                   'Brass 2': [8, 61],
                   'Synth Brass 3': [8, 62],
                   'Synth Brass 4': [8, 63],
                   'Sine Wave': [8, 80],
                   'Taisho Koto': [8, 107],
                   'Castanets': [8, 115],
                   'Concert Bass Drum': [8, 116],
                   'Melo Tom 2': [8, 117],
                   '808 Tom': [8, 118],
                   'Burst Noise': [9, 125],
                   'Mandolin': [16, 25],
                   'Standard': [128, 0],
                   'Standard 1': [128, 1],
                   'Standard 2': [128, 2],
                   'Standard 3': [128, 3],
                   'Standard 4': [128, 4],
                   'Standard 5': [128, 5],
                   'Standard 6': [128, 6],
                   'Standard 7': [128, 7],
                   'Room': [128, 8],
                   'Room 1': [128, 9],
                   'Room 2': [128, 10],
                   'Room 3': [128, 11],
                   'Room 4': [128, 12],
                   'Room 5': [128, 13],
                   'Room 6': [128, 14],
                   'Room 7': [128, 15],
                   'Power': [128, 16],
                   'Power 1': [128, 17],
                   'Power 2': [128, 18],
                   'Power 3': [128, 19],
                   'Electronic': [128, 24],
                   'TR-808': [128, 25],
                   'Jazz': [128, 32],
                   'Jazz 1': [128, 33],
                   'Jazz 2': [128, 34],
                   'Jazz 3': [128, 35],
                   'Jazz 4': [128, 36],
                   'Brush': [128, 40],
                   'Brush 1': [128, 41],
                   'Brush 2': [128, 42],
                   'Orchestra Kit': [128, 48]}

#### NAMEDTUPLE DEFINITIONS ####
PercussionInstrument = namedtuple("Instrument",
                                  ["name", "note"])

Instrument = namedtuple("Instrument",
                        ["name", "bank", "prog"])

#### DATACLASS DEFINITIONS ####

@dataclass
class GmPercussion:
    high_q: PercussionInstrument
    slap: PercussionInstrument
    scratch_push: PercussionInstrument
    scratch_pull: PercussionInstrument
    sticks: PercussionInstrument
    square_click: PercussionInstrument
    metronome_click: PercussionInstrument
    metronome_bell: PercussionInstrument
    acoustic_bass_drum: PercussionInstrument
    electric_bass_drum: PercussionInstrument
    side_stick: PercussionInstrument
    acoustic_snare: PercussionInstrument
    hand_clap: PercussionInstrument
    electric_snare: PercussionInstrument
    low_floor_tom: PercussionInstrument
    closed_hi_hat: PercussionInstrument
    high_floor_tom: PercussionInstrument
    pedal_hi_hat: PercussionInstrument
    low_tom: PercussionInstrument
    open_hi_hat: PercussionInstrument
    low_mid_tom: PercussionInstrument
    hi_mid_tom: PercussionInstrument
    crash_cymbal_1: PercussionInstrument
    high_tom: PercussionInstrument
    ride_cymbal_1: PercussionInstrument
    chinese_cymbal: PercussionInstrument
    ride_bell: PercussionInstrument
    tambourine: PercussionInstrument
    splash_cymbal: PercussionInstrument
    cowbell: PercussionInstrument
    crash_cymbal_2: PercussionInstrument
    vibra_slap: PercussionInstrument
    ride_cymbal_2: PercussionInstrument
    high_bongo: PercussionInstrument
    low_bongo: PercussionInstrument
    mute_high_conga: PercussionInstrument
    open_high_conga: PercussionInstrument
    low_conga: PercussionInstrument
    high_timbale: PercussionInstrument
    low_timbale: PercussionInstrument
    high_agogo: PercussionInstrument
    low_agogo: PercussionInstrument
    cabasa: PercussionInstrument
    maracas: PercussionInstrument
    short_whistle: PercussionInstrument
    long_whistle: PercussionInstrument
    short_guiro: PercussionInstrument
    long_guiro: PercussionInstrument
    claves: PercussionInstrument
    high_woodblock: PercussionInstrument
    low_woodblock: PercussionInstrument
    mute_cuica: PercussionInstrument
    open_cuica: PercussionInstrument
    mute_triangle: PercussionInstrument
    open_triangle: PercussionInstrument
    shaker: PercussionInstrument
    jingle_bell: PercussionInstrument
    belltree: PercussionInstrument
    castanets: PercussionInstrument
    mute_surdo: PercussionInstrument
    open_surdo: PercussionInstrument

    def __init__(self, attribute_dict):
        for param, instrument in attribute_dict.items():
            object.__setattr__(self, param, instrument)


@dataclass
class FluidSoundFont:
    yamaha_grand_piano: Instrument
    bright_yamaha_grand: Instrument
    electric_piano: Instrument
    honky_tonk: Instrument
    rhodes_ep: Instrument
    legend_ep_2: Instrument
    harpsichord: Instrument
    clavinet: Instrument
    celesta: Instrument
    glockenspiel: Instrument
    music_box: Instrument
    vibraphone: Instrument
    marimba: Instrument
    xylophone: Instrument
    tubular_bells: Instrument
    dulcimer: Instrument
    drawbarorgan: Instrument
    percussive_organ: Instrument
    rock_organ: Instrument
    church_organ: Instrument
    reed_organ: Instrument
    accordian: Instrument
    harmonica: Instrument
    bandoneon: Instrument
    nylon_string_guitar: Instrument
    steel_string_guitar: Instrument
    jazz_guitar: Instrument
    clean_guitar: Instrument
    palm_muted_guitar: Instrument
    overdrive_guitar: Instrument
    distortion_guitar: Instrument
    guitar_harmonics: Instrument
    acoustic_bass: Instrument
    fingered_bass: Instrument
    picked_bass: Instrument
    fretless_bass: Instrument
    slap_bass: Instrument
    pop_bass: Instrument
    synth_bass_1: Instrument
    synth_bass_2: Instrument
    violin: Instrument
    viola: Instrument
    cello: Instrument
    contrabass: Instrument
    tremolo: Instrument
    pizzicato_section: Instrument
    harp: Instrument
    timpani: Instrument
    strings: Instrument
    slow_strings: Instrument
    synth_strings_1: Instrument
    synth_strings_2: Instrument
    ahh_choir: Instrument
    ohh_voices: Instrument
    synth_voice: Instrument
    orchestra_hit: Instrument
    trumpet: Instrument
    trombone: Instrument
    tuba: Instrument
    muted_trumpet: Instrument
    french_horns: Instrument
    brass_section: Instrument
    synth_brass_1: Instrument
    synth_brass_2: Instrument
    soprano_sax: Instrument
    alto_sax: Instrument
    tenor_sax: Instrument
    baritone_sax: Instrument
    oboe: Instrument
    english_horn: Instrument
    bassoon: Instrument
    clarinet: Instrument
    piccolo: Instrument
    flute: Instrument
    recorder: Instrument
    pan_flute: Instrument
    bottle_chiff: Instrument
    shakuhachi: Instrument
    whistle: Instrument
    ocarina: Instrument
    square_lead: Instrument
    saw_wave: Instrument
    calliope_lead: Instrument
    chiffer_lead: Instrument
    charang: Instrument
    solo_vox: Instrument
    fifth_sawtooth_wave: Instrument
    bass_and_lead: Instrument
    fantasia: Instrument
    warm_pad: Instrument
    polysynth: Instrument
    space_voice: Instrument
    bowed_glass: Instrument
    metal_pad: Instrument
    halo_pad: Instrument
    sweep_pad: Instrument
    ice_rain: Instrument
    soundtrack: Instrument
    crystal: Instrument
    atmosphere: Instrument
    brightness: Instrument
    goblin: Instrument
    echo_drops: Instrument
    star_theme: Instrument
    sitar: Instrument
    banjo: Instrument
    shamisen: Instrument
    koto: Instrument
    kalimba: Instrument
    bagpipe: Instrument
    fiddle: Instrument
    shenai: Instrument
    tinker_bell: Instrument
    agogo: Instrument
    steel_drums: Instrument
    woodblock: Instrument
    taiko_drum: Instrument
    melodic_tom: Instrument
    synth_drum: Instrument
    reverse_cymbal: Instrument
    fret_noise: Instrument
    breath_noise: Instrument
    sea_shore: Instrument
    bird_tweet: Instrument
    telephone: Instrument
    helicopter: Instrument
    applause: Instrument
    gun_shot: Instrument
    detuned_ep_1: Instrument
    detuned_ep_2: Instrument
    coupled_harpsichord: Instrument
    church_bell: Instrument
    detuned_organ_1: Instrument
    detuned_organ_2: Instrument
    church_organ_2: Instrument
    italian_accordion: Instrument
    ukulele: Instrument
    guitar_12_string: Instrument
    hawaiian_guitar: Instrument
    funk_guitar: Instrument
    feedback_guitar: Instrument
    guitar_feedback: Instrument
    synth_bass_3: Instrument
    synth_bass_4: Instrument
    slow_violin: Instrument
    orchestral_pad: Instrument
    synth_strings_3: Instrument
    brass_2: Instrument
    synth_brass_3: Instrument
    synth_brass_4: Instrument
    sine_wave: Instrument
    taisho_koto: Instrument
    castanets: Instrument
    concert_bass_drum: Instrument
    melo_tom_2: Instrument
    tom_808: Instrument
    burst_noise: Instrument
    mandolin: Instrument
    standard: Instrument
    standard_1: Instrument
    standard_2: Instrument
    standard_3: Instrument
    standard_4: Instrument
    standard_5: Instrument
    standard_6: Instrument
    standard_7: Instrument
    room: Instrument
    room_1: Instrument
    room_2: Instrument
    room_3: Instrument
    room_4: Instrument
    room_5: Instrument
    room_6: Instrument
    room_7: Instrument
    power: Instrument
    power_1: Instrument
    power_2: Instrument
    power_3: Instrument
    electronic: Instrument
    tr_808: Instrument
    jazz: Instrument
    jazz_1: Instrument
    jazz_2: Instrument
    jazz_3: Instrument
    jazz_4: Instrument
    brush: Instrument
    brush_1: Instrument
    brush_2: Instrument
    orchestra_kit: Instrument

    def __init__(self, attribute_dict):
        for param, instrument in attribute_dict.items():
            object.__setattr__(self, param, instrument)


#### ATTRIBUTE DICTIONARIES ####

gm_percussion_attr_dict = {}
for name, note in C.GM_PERCUSSION_DICT.items():
    param_name = name.lower()
    param_name = param_name.replace(" ", "_")
    param_name = param_name.replace("-", "_")
    inst = PercussionInstrument(name, note)
    gm_percussion_attr_dict[param_name] = inst

fs_attr_dict = {}
for name, info in FLUIDR3_GM_DICT.items():

    # handle special cases
    if name == '12 String Guitar':
        param_name = 'guitar_12_string'
        fs_attr_dict[param_name] = Instrument(name=name,
                                              bank=info[0],
                                              prog=info[1])
    elif name == '808 Tom':
        param_name = 'tom_808'
        fs_attr_dict[param_name] = Instrument(name=name,
                                              bank=info[0],
                                              prog=info[1])
    elif name == 'Bass & Lead':
        param_name = 'bass_and_lead'
        fs_attr_dict[param_name] = Instrument(name=name,
                                              bank=info[0],
                                              prog=info[1])
    else:
        param_name = name.lower().replace(" ", "_").replace("-", "_")

        fs_attr_dict[param_name] = Instrument(name=name,
                                              bank=info[0],
                                              prog=info[1])

#### INSTANCE CREATION ####

FluidInstrumentRack = FluidSoundFont(attribute_dict=fs_attr_dict)
GmPercussionRack = GmPercussion(attribute_dict=gm_percussion_attr_dict)


