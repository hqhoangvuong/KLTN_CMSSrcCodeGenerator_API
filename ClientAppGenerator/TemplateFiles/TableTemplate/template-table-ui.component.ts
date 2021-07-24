import {
  Component,
  OnInit,
  Output,
  EventEmitter,
  HostListener,
  Inject,
} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { PageEvent } from '@angular/material/paginator';
import { ThemeServiceService } from '../../../style-service/theme-service.service';
import { [--ModelName--]DeleteUIComponent } from '[--DeleteUiComponent--]';
import { ToastrService } from 'ngx-toastr';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { [--ServiceName--], [--ModelName--] } from '[--ClientApiPackageName--]';

@Component({
  selector: '[--SelectorName--]',
  templateUrl: './[--UrlName--].html',
  styleUrls: ['./[--UrlName--].scss'],
})

export class [--ModelName--]TableUIComponent implements OnInit {
  _service: [--ServiceName--];
  modelDisplayName: string;
  listItems: [--ModelName--][] = [];
  @Output() nameActionTrigger = new EventEmitter<any>();
  contentType: string[] = ['text/html', 'charset=UTF-8'];
  pageIndex: number = 1;
  pageSize: number = 10;
  pageDataTotalCount: number;
  pageEvent: PageEvent;
  map: { [key: string]: string } = {};
  string: [] = [];
  token: any;
  httpClient: HttpClient;
  isDarkThemeSubscription: boolean = false;
  isFiltering: boolean=false;
  filterKey: string= ''

  constructor(
    private themeService: ThemeServiceService,
    public dialog: MatDialog,
    private toastr: ToastrService,
    @Inject([--ServiceName--]) _service: [--ServiceName--]
  ) {
    this.checkTheme();
    this.token = localStorage.getItem('accessToken');
    _service.defaultHeaders = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ` + this.token,
    });
    this._service = _service;
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

  ngOnInit(): void {
    this.checkTheme();
    this.getPagingApi(this.pageIndex, this.pageSize);
    this.getAllApi();
  }

  getPagingApi(pageIndex: number, pageSize: number) {
    this._service
      .api[--ModelName--]PagingGet(pageIndex, pageSize)
      .subscribe((result) => {
        this.listItems = result;
      });
  }

  getAllApi() {
    this._service.api[--ModelName--]PagingGet(0, 10).subscribe((result) => {
      this.pageDataTotalCount = Object.keys(result).length;
    });
  }

  /** [--IsDisableUpdate--]
  onClickEdit(id: any) {
    this.nameActionTrigger.emit({ type: 'edit', idItem: id });
  }
  [--IsDisableUpdate--] */

  reGetPagingData() {
    this.getPagingApi(this.pageIndex, this.pageSize);
  }

  gotoPrevious() {
    var sizePrevious = 0;
    sizePrevious = this.pageSize - 10;
    if (sizePrevious > 0) {
      this.pageSize = sizePrevious;
      this.getPagingApi(this.pageIndex, this.pageSize);
    }
  }

  gotoNext() {
    var sizeNext = 0;
    sizeNext =+ this.pageSize + +10;
    if (sizeNext > 0) {
      this.pageSize = sizeNext;
      this.getPagingApi(this.pageIndex, this.pageSize);
    }
  }

  /** [--IsDisableDelete--]
  onClickDelete([--PrimaryKey--]: any) {
    const dialogRef = this.dialog.open([--ModelName--]DeleteUIComponent, {
      data: { idSelected: [--PrimaryKey--] },
    });
    dialogRef.afterClosed().subscribe((result) => {
      if (result.data) {
        this._service.api[--ModelName--]Delete([--PrimaryKey--]).subscribe(
          (res) => {
            this.toastr.success("Delete successfully", "Notification");
            this.getPagingApi(this.pageIndex, this.pageSize);
            this.getAllApi();
          },
          (err) => {
            if (err.status === 400) {
              this.toastr.warning(err.error, 'Warning');
            }
          }
        );
      }
    });
  }
  [--IsDisableDelete--] */

  onClickView([--PrimaryKey--]: any) {
    this.nameActionTrigger.emit({ type: 'read', idItem: [--PrimaryKey--] });
  }

  async applyFilter(event: any) {
    if (this.filterKey === '' ) {
      this.ngOnInit();
    } else if (event.code === 'Backspace') {
      this.ngOnInit();
      this.listItems = this.listItems.filter(item => {
        return ("" + item.[--PrimaryKey--]).trim().toLocaleLowerCase().includes(this.filterKey.toLocaleLowerCase());
      })
    } else{
      this.listItems = this.listItems.filter(item => {
        return ("" + item.[--PrimaryKey--]).trim().toLocaleLowerCase().includes(this.filterKey.toLocaleLowerCase());
      })
   }
  }
}

export interface DialogData {
  idSelected: any;
}
