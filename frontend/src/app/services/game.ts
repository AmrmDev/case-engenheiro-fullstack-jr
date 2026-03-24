import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Game, AttemptResult, RankingEntry } from '../models/game';

@Injectable({
  providedIn: 'root'
})
export class GameService {
  private apiUrl = 'http://localhost:8000/api/games';

  constructor(private http: HttpClient) {}

  startGame(): Observable<Game> {
    return this.http.post<Game>(`${this.apiUrl}/`, {});
  }

  submitAttempt(gameId: number, guess: string[]): Observable<AttemptResult> {
    return this.http.post<AttemptResult>(
      `${this.apiUrl}/${gameId}/attempts`,
      { guess }
    );
  }

  getHistory(): Observable<Game[]> {
    return this.http.get<Game[]>(`${this.apiUrl}/`);
  }

  getGameDetail(gameId: number): Observable<Game> {
    return this.http.get<Game>(`${this.apiUrl}/${gameId}`);
  }

  getRanking(): Observable<RankingEntry[]> {
    return this.http.get<RankingEntry[]>(`${this.apiUrl}/ranking/top`);
  }
}