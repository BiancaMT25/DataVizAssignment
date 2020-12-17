
constructor_map_engines = {'alfa romeo': ['sauber', 'bmw sauber', 'alfa', 'alfa romeo', 'alfa romeo racing'],
                            'alphatauri': ['minardi', 'toro rosso', 'alphatauri', 'scuderia toro rosso'],
                            'mclaren': ['mclaren'],
                            'mercedes': ['mercedes', 'tyrrell', 'bar', 'brawn', 'honda'],
                            'racing point': ['racing point', 'force india', 'jordan', 'spyker', 'mf1', 'forceindia'],
                            'red bull': ['red bull', 'stewart', 'jaguar', 'red bull racing'],
                            'renault': ['renault', 'renault[18]', 'toleman', 'benetton', 'lotus'],
                            'ferrari': ['ferrari'],
                            'haas f1 team': ['haas'],
                            'williams': ['williams'],
                            'manor marussia': ['mrt']}

reversed_constructor_map_engines = {}
for k, v in constructor_map_engines.items():
    for element in v:
        reversed_constructor_map_engines[element] = k

constructor_map = {'alfa': ['sauber', 'bmw_sauber', 'alfa'],
                   'alphatauri': ['alpha_tauri', 'minardi', 'toro_rosso', 'alphatauri'],
                   'mclaren': ['mclaren', 'mclaren-alfa_romeo', 'mclaren-brm', 'mclaren-ford', 'mclaren-seren'],
                   'mercedes': ['mercedes', 'tyrrell', 'bar', 'brawn', 'honda'],
                   'racing_point': ['racing_point', 'force_india', 'jordan', 'spyker', 'spyker_mf1', 'mf1'],
                   'red_bull': ['red_bull', 'stewart', 'jaguar'],
                   'renault': ['renault', 'toleman', 'benetton', 'lotus_racing', 'lotus_f1'],
                   'ferrari': ['ferrari'],
                   'haas': ['haas'],
                   'williams': ['williams'],}

# reverse dictionary
reversed_constructor_map = {}
for k, v in constructor_map.items():
    for element in v:
        reversed_constructor_map[element] = k