import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateUIComponent } from './create-ui.component';

describe('CreateUIComponent', () => {
  let component: CreateUIComponent;
  let fixture: ComponentFixture<CreateUIComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CreateUIComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateUIComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
