import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IndexUIComponent } from './index-ui.component';

describe('IndexUIComponent', () => {
  let component: IndexUIComponent;
  let fixture: ComponentFixture<IndexUIComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ IndexUIComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(IndexUIComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
