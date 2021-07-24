import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ThemeServiceService {

  isThemeDark: Subject<boolean> = new Subject<boolean>();
  getDarkTheme(){
    return this.isThemeDark.asObservable();
  }
  constructor() { }
  setDarkTheme(isThemeDark: boolean) {
    this.isThemeDark.next(isThemeDark);
    if (isThemeDark == true) {
      localStorage.setItem('dark', 'true');
    }
    else {
      localStorage.setItem('dark', 'false');
    }
  }
}
