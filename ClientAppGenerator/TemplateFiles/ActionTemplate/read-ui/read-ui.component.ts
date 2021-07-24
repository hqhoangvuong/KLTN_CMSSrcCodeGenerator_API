import { Component, Input, OnInit, Inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { [--ServiceName--], [--ModelName--] } from '[--ApiClientPackageId--]';
import { ThemeServiceService } from '../../../../../style-service/theme-service.service';

@Component({
  selector: "[--SelectorName--]",
  templateUrl: "./[--UrlName--].html",
  styleUrls: ["./[--UrlName--].scss"],
})

export class [--ClassName--] implements OnInit {
  service: [--ServiceName--];
  isDarkThemeSubscription: boolean=false;
  item: [--ModelName--];
  idSelectedInput = '';
  idSelectedInputNumber: number;
  constructor(private themeService: ThemeServiceService,
    @Inject([--ServiceName--]) srv: [--ServiceName--],
    private route: ActivatedRoute) {
    this.service = srv;
    this.checkTheme();
    this.idSelectedInputNumber = -1;
  }

  ngOnInit(): void {
    this.idSelectedInput = this.route.snapshot.paramMap.get('id');
    this.idSelectedInputNumber = (+ this.idSelectedInput);
    this.getItemById();
  }

  getItemById() {
    this.service.api[--ModelName--]IdGet([--CastedIdSelectInput--]).subscribe(data => {
      this.item = data;
    })
  }

  checkTheme() {
    this.themeService.getDarkTheme().subscribe((ok) => {
      this.isDarkThemeSubscription = ok;
    });
    if (localStorage.getItem('dark') == 'true') {
      this.isDarkThemeSubscription = true;
    } else {
      this.isDarkThemeSubscription = false;
    }
  }
}
