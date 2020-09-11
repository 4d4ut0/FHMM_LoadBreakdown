package com.testobject.httprequest.respHorimetroConsumo;

import java.util.ArrayList;

public class respHorimetroConsumo {
    private ArrayList<ConsumoHorimetro> dentroDoHorario;
    private ArrayList<ConsumoHorimetro> foraDoHorario;

    public ArrayList<ConsumoHorimetro> getDentroDoHorario() {
        return dentroDoHorario;
    }

    public void setDentroDoHorario(ArrayList<ConsumoHorimetro> dentroDoHorario) {
        this.dentroDoHorario = dentroDoHorario;
    }

    public ArrayList<ConsumoHorimetro> getForaDoHorario() {
        return foraDoHorario;
    }

    public void setForaDoHorario(ArrayList<ConsumoHorimetro> foraDoHorario) {
        this.foraDoHorario = foraDoHorario;
    }
}
