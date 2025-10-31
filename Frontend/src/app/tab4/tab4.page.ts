import { Component } from '@angular/core';
import { IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-tab4',
  templateUrl: 'tab4.page.html',
  styleUrls: ['tab4.page.scss'],
  imports: [IonicModule, CommonModule, FormsModule],
})
export class Tab4Page {
  nombre = 'María Gómez';
  correo = 'maria.gomez@colegio.com';
  materias = ['Matemáticas', 'Ciencias Naturales', 'Lengua Castellana'];

  estudiantes = [
    { nombre: 'Juan Pérez' },
    { nombre: 'Ana Torres' },
    { nombre: 'Luis Díaz' },
    { nombre: 'Laura Mejía' }
  ];

  registros: any[] = [];

  constructor() {
    this.generarRegistros();
  }

  generarRegistros() {
    // Por cada estudiante, genera una nota para cada materia
    this.estudiantes.forEach((est) => {
      this.materias.forEach((mat) => {
        this.registros.push({
          estudiante: est.nombre,
          materia: mat,
          nota: this.generarNotaAleatoria()
        });
      });
    });
  }

  generarNotaAleatoria(): number {
    // Genera una nota entre 2.5 y 5.0 con dos decimales
    return Number.parseFloat((Math.random() * (5 - 2.5) + 2.5).toFixed(1));
  }
}
