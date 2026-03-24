import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { Token, LoginRequest, RegisterRequest, User } from '../models/user';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api/auth';

  constructor(private http: HttpClient, private router: Router) {}

  register(data: RegisterRequest): Observable<Token> {
    return this.http.post<Token>(`${this.apiUrl}/register`, data).pipe(
      tap(response => this.saveToken(response.access_token))
    );
  }

  login(data: LoginRequest): Observable<Token> {
    return this.http.post<Token>(`${this.apiUrl}/login`, data).pipe(
      tap(response => this.saveToken(response.access_token))
    );
  }

  getMe(): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/me`);
  }

  logout(): void {
    localStorage.removeItem('token');
    this.router.navigate(['/login']);
  }

  saveToken(token: string): void {
    localStorage.setItem('token', token);
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }
}