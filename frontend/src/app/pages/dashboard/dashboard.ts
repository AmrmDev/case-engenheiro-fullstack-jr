import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth';
import { GameService } from '../../services/game';
import { Header } from '../../components/header/header';
import { User } from '../../models/user';
import { Game } from '../../models/game';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink, Header],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.scss']
})
export class Dashboard implements OnInit {
  user: User | null = null;
  recentGames: Game[] = [];
  loading = true;
  startingGame = false;

constructor(
  private authService: AuthService,
  private gameService: GameService,
  private router: Router,
  private cdr: ChangeDetectorRef
) {}

  ngOnInit(): void {
    this.authService.getMe().subscribe({
      next: (user) => { this.user = user; this.cdr.detectChanges(); },
      error: () => {}
    });

    this.gameService.getHistory().subscribe({
      next: (games) => {
        this.recentGames = games.slice(0, 5);
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: () => { this.loading = false; this.cdr.detectChanges(); }
    });
  }

  get wonCount(): number {
    return this.recentGames.filter(g => g.won).length;
  }

  startNewGame(): void {
    this.startingGame = true;
    this.gameService.startGame().subscribe({
      next: (game) => this.router.navigate(['/game'], { state: { gameId: game.id } }),
      error: () => { this.startingGame = false; }
    });
  }

  formatDuration(seconds: number): string {
    if (!seconds) return '—';
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return m > 0 ? `${m}m ${s}s` : `${s}s`;
  }

  formatDate(dateStr: string): string {
    return new Date(dateStr).toLocaleDateString('pt-BR', {
      day: '2-digit', month: '2-digit', year: '2-digit',
      hour: '2-digit', minute: '2-digit'
    });
  }
}