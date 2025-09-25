import requests
import pandas as pd

def get_current_players(appid):
    """Busca o número de jogadores atuais para um AppID específico"""
    url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'response' in data and 'player_count' in data['response']:
                return data['response']['player_count']
    except:
        pass
    return 0

def load_app_catalog():
    """Carrega o catálogo de apps da Steam (appid -> name) para evitar falhas do appdetails."""
    catalog_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    try:
        r = requests.get(catalog_url, timeout=10)
        if r.status_code == 200:
            payload = r.json()
            apps = payload.get("applist", {}).get("apps", [])
            # Constrói um dicionário {appid: name}
            return {app.get("appid"): app.get("name", "").strip() for app in apps}
    except Exception:
        pass
    return {}

def scrape_steam_trending():
    # URL oficial da Steam Charts (Most Played)
    url = "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/"

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Erro ao acessar {url}, código: {response.status_code}")

    data = response.json()
    games = data["response"]["ranks"]

    games_data = []
    for game in games:
        games_data.append({
            "Posição": game.get("rank", 0),
            "AppID": game.get("appid", 0),
        })

    # Carrega o catálogo completo de apps para mapear nomes rapidamente
    appid_to_name = load_app_catalog()

    # Buscar nomes dos jogos e número de jogadores atuais
    game_names = []
    for i, g in enumerate(games_data):
        appid = g["AppID"]

        # Primeiro tenta via catálogo
        title = appid_to_name.get(appid, "").strip() if appid_to_name else ""

        # Se não encontrou no catálogo, tenta via appdetails como fallback
        if not title:
            info_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=en"
            try:
                r = requests.get(info_url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
                if r.status_code == 200:
                    info = r.json()
                    if str(appid) in info and info[str(appid)].get("success"):
                        title = info[str(appid)]["data"].get("name", "")
            except Exception:
                pass

        g["Título"] = title if title else "N/A"
        
        # Buscar número de jogadores atuais
        g["Jogadores Atuais"] = get_current_players(appid)
        
        game_names.append(g)
        print(f"Processado {i+1}/{len(games_data)}: {g['Título']} - {g['Jogadores Atuais']} jogadores")

    # Ordenar por número de jogadores (maior para menor)
    df = pd.DataFrame(game_names, columns=["Posição", "Título", "AppID", "Jogadores Atuais"])
    df = df.sort_values("Jogadores Atuais", ascending=False).reset_index(drop=True)
    
    # Renumerar as posições baseado na nova ordem
    df["Posição"] = range(1, len(df) + 1)
    
    df.to_csv("jogos_steam.csv", index=False, encoding="utf-8-sig")

    print("Arquivo 'jogos_steam.csv' gerado com sucesso!")
    print(f"Top 5 jogos por número de jogadores:")
    for i in range(min(5, len(df))):
        print(f"{df.iloc[i]['Posição']}. {df.iloc[i]['Título']} - {df.iloc[i]['Jogadores Atuais']:,} jogadores")


if __name__ == "__main__":
    scrape_steam_trending()
