import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { GameService } from '../../services/game';
import { Header } from '../../components/header/header';
import { AttemptResult } from '../../models/game';


export type Color = 'A' | 'B' | 'C' | 'D' | 'E' | 'F';

export interface AttemptRow {
  guess: Color[];
  exact_hits: number;
  attempt_number: number;
}

const COLORS: Color[] = ['A', 'B', 'C', 'D', 'E', 'F'];
const MAX_ATTEMPTS = 10;
const CODE_LENGTH = 4;

@Component({
  selector: 'app-game',
  standalone: true,
  imports: [CommonModule, Header],
  templateUrl: './game.html',
  styleUrls: ['./game.scss']
})
export class Game implements OnInit {
  colors = COLORS;
  codeLength = CODE_LENGTH;
  maxAttempts = MAX_ATTEMPTS;
  slots = Array(CODE_LENGTH).fill(null);

  gameId: number | null = null;
  attempts: AttemptRow[] = [];
  currentGuess: (Color | null)[] = Array(CODE_LENGTH).fill(null);
  selectedColor: Color | null = null;

  loading = true;
  submitting = false;
  error = '';
  gameOver = false;
  won = false;
  finalScore: number | null = null;

  colorMap: Record<Color, { bg: string; label: string }> = {
    A: { bg: '#ef4444', label: 'Vermelho' },
    B: { bg: '#3b82f6', label: 'Azul' },
    C: { bg: '#22c55e', label: 'Verde' },
    D: { bg: '#f59e0b', label: 'Amarelo' },
    E: { bg: '#a855f7', label: 'Roxo' },
    F: { bg: '#f97316', label: 'Laranja' },
  };

constructor(private gameService: GameService, private router: Router, private cdr: ChangeDetectorRef) {}
  ngOnInit(): void {
    const nav = history.state;
    if (nav?.gameId) {
      this.gameId = nav.gameId;
      this.loading = false;
    } else {
      this.startNewGame();
    }
  }

  startNewGame(): void {
    this.loading = true;
    this.gameService.startGame().subscribe({
      next: (game) => {
        this.gameId = game.id;
        this.attempts = [];
        this.currentGuess = Array(CODE_LENGTH).fill(null);
        this.gameOver = false;
        this.won = false;
        this.finalScore = null;
        this.loading = false;
      },
      error: () => {
        this.error = 'Erro ao iniciar partida.';
        this.loading = false;
      }
    });
  }

  selectColor(color: Color): void {
    this.selectedColor = color;
  }

  placeColor(slotIndex: number): void {
    if (!this.selectedColor || this.gameOver) return;
    this.currentGuess = [...this.currentGuess];
    this.currentGuess[slotIndex] = this.selectedColor;
  }

  clearSlot(slotIndex: number): void {
    if (this.gameOver) return;
    this.currentGuess = [...this.currentGuess];
    this.currentGuess[slotIndex] = null;
  }

  get canSubmit(): boolean {
    return this.currentGuess.every(c => c !== null) && !this.submitting && !this.gameOver;
  }

  get attemptsLeft(): number {
    return MAX_ATTEMPTS - this.attempts.length;
  }

  submitGuess(): void {
    if (!this.canSubmit || !this.gameId) return;
    this.submitting = true;
    this.error = '';

    const guess = this.currentGuess as Color[];
    this.gameService.submitAttempt(this.gameId, guess).subscribe({
      next: (result: AttemptResult) => {
        this.attempts = [...this.attempts, {
          guess: [...guess],
          exact_hits: result.exact_hits,
          attempt_number: result.attempt_number
        }];
        this.currentGuess = Array(CODE_LENGTH).fill(null);
        this.submitting = false;  
        this.cdr.detectChanges();  // <- adiciona essa linha

        if (result.game_over) {
          this.gameOver = true;
          this.won = result.won;
          this.finalScore = result.score;
          this.cdr.detectChanges();  // <- e essa também
        }
      },
      error: (err) => {
        this.error = err.error?.detail || 'Erro ao enviar tentativa.';
        this.submitting = false;
      }
    });
  }

  getHitDots(hits: number): number[] { return Array(hits).fill(0); }
  getMissDots(attempt: AttemptRow): number[] { return Array(CODE_LENGTH - attempt.exact_hits).fill(0); }
  colorOf(c: Color | null): string { return c ? (this.colorMap[c]?.bg ?? '#555') : 'transparent'; }
  goToDashboard(): void { this.router.navigate(['/dashboard']); }
}