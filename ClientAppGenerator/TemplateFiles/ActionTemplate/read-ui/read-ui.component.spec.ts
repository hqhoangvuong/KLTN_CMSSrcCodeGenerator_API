import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReadUIComponent } from './read-ui.component';

describe('ReadUIComponent', () => {
  let component: ReadUIComponent;
  let fixture: ComponentFixture<ReadUIComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ReadUIComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ReadUIComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
