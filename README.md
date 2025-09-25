# Steam Scraper - Jogos Mais Populares 🎮

## 5W1H

### **Who (Quem?)**
O projeto foi desenvolvido para estudantes, entusiastas de programação e análise de dados que desejam **explorar os jogos mais jogados da Steam** de forma automatizada e estruturada.

---

### **What (O quê?)**
Um coletor de dados (scraper) que acessa a API pública da **Steam**, coleta informações dos jogos mais jogados no momento e gera um arquivo CSV com:
- Posição no ranking
- Título do jogo
- AppID
- Número de jogadores atuais

---

### **Where (Onde?)**
Os dados são obtidos diretamente da API oficial da **Steam**:
- [GetMostPlayedGames](https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/)
- [GetAppList](https://api.steampowered.com/ISteamApps/GetAppList/v2/)
- [GetNumberOfCurrentPlayers](https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/)

---

### **When (Quando?)**
O scraper pode ser executado a qualquer momento.  
Cada execução coleta os **dados mais recentes** disponíveis na Steam no instante da consulta.

---

### **Why (Por quê?)**
- Para **analisar tendências** no mercado de jogos digitais.  
- Auxiliar em estudos de **Data Science** e **Machine Learning** com dados reais.  
- Facilitar a criação de relatórios ou dashboards de popularidade dos jogos.

---

### **How (Como?)**
1. Clone o repositório:
   git clone https://github.com/GabrielNolasco-hub/steam-scrapper.git
2.
  cd steam-scraper




   
