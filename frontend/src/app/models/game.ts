export interface Game {
  id: number;
  user_id: number;
  score: number;
  duration_seconds: number;
  finished: boolean;
  won: boolean;
  created_at: string;
}

export interface AttemptResult {
  attempt_number: number;
  exact_hits: number;
  game_over: boolean;
  won: boolean;
  score: number | null;
}

export interface RankingEntry {
  username: string;
  best_score: number;
  total_games: number;
}