import pygame
import db

def save_game_result(username, score, level):
    try:
        conn = db.get_connection()
        cur = conn.cursor()
        u_clean = "".join(i for i in username if ord(i) < 128)
        cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING;", (u_clean,))
        cur.execute("SELECT id FROM players WHERE username = %s;", (u_clean,))
        p_id = cur.fetchone()[0]
        cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s);", (p_id, score, level))
        conn.commit()
        cur.close(); conn.close()
    except Exception as e:
        print(f"Database error: {e}")

def get_top_scores():
    try:
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.username, s.score FROM game_sessions s 
            JOIN players p ON s.player_id = p.id 
            ORDER BY s.score DESC LIMIT 10;
        """)
        rows = cur.fetchall()
        cur.close(); conn.close()
        return rows
    except:
        return []

def get_personal_best(username):
    try:
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT MAX(s.score) FROM game_sessions s 
            JOIN players p ON s.player_id = p.id 
            WHERE p.username = %s;
        """, (username,))
        res = cur.fetchone()[0]
        cur.close(); conn.close()
        return res if res else 0
    except:
        return 0

def show_leaderboard(dis):
    tops = get_top_scores()
    font = pygame.font.SysFont("verdana", 18)
    title_font = pygame.font.SysFont("verdana", 24, bold=True)
    
    while True:
        dis.fill((0, 0, 0)) # BLACK
        dis.blit(title_font.render("TOP 10 LEADERBOARD", True, (255, 215, 0)), [150, 30])
        
        for i, (name, score) in enumerate(tops):
            txt = f"{i+1}. {name}: {score}"
            dis.blit(font.render(txt, True, (255, 255, 255)), [150, 80 + (i * 25)])
            
        dis.blit(font.render("Press C to Restart or Q to Quit", True, (213, 50, 80)), [140, 360])
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return # Goes back to main loop to restart
                if event.key == pygame.K_q:
                    pygame.quit(); exit()