import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GameService } from '../../services/game';
import { Header } from '../../components/header/header';
import { RankingEntry } from '../../models/game';

@Component({
  selector: 'app-ranking',
  standalone: true,
  imports: [CommonModule, Header],
  templateUrl: './ranking.html',
  styleUrls: ['./ranking.scss']
})
export class Ranking implements OnInit {
  entries: RankingEntry[] = [];
  loading = true;
  error = '';

  constructor(private gameService: GameService, private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.gameService.getRanking().subscribe({
      next: (data) => {
        this.entries = data;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.error = 'Erro ao carregar ranking.';
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }

  getMedal(index: number): string {
    return ['🥇', '🥈', '🥉'][index] ?? '';
  }
}