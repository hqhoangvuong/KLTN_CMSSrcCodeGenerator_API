import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { ThemeServiceService } from '../../style-service/theme-service.service';

@Component({
  selector: 'app-index-ui',
  templateUrl: './index-ui.component.html',
  styleUrls: ['./index-ui.component.scss'],
})
export class IndexUIComponent implements OnInit {
  isDarkMode: boolean = true;

  actionNameTriggered: string = '';

  isDarkThemeSubscription: boolean = false;

  ctrl = new FormControl(false);

  idSelected: any;

  constructor(private themeSerive: ThemeServiceService) {
    this.checkTheme();
  }

  checkTheme() {
    this.themeSerive.getDarkTheme().subscribe((ok) => {
      this.isDarkThemeSubscription = ok;
    });
    if (localStorage.getItem('dark') == 'true') {
      this.ctrl.disabled;
      this.isDarkThemeSubscription = true;
    } else {
      this.ctrl.enabled;
      this.isDarkThemeSubscription = false;
    }
  }

  ngOnInit(): void {
    this.checkTheme();
  }

  switchMode() {
    this.themeSerive.setDarkTheme(this.isDarkMode);
    this.isDarkMode = !this.isDarkMode;
  }

  getActionTrigger($event: any) {
    this.actionNameTriggered = $event.type;
    this.idSelected = $event.idItem;
  }

  onTriggerAction(item: string) {
    this.actionNameTriggered = item;
  }
}
