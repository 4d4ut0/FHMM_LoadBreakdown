package com.testobject.httprequest.respConsumo;

import java.util.ArrayList;

public class respConsumo {
    private ArrayList<Consumo> consumo;
    private String consumoMensal;
    private String mensagem;

    public ArrayList<Consumo> getConsumos() {
        return consumo;
    }

    public void setConsumos(ArrayList<Consumo> consumos) {
        this.consumo = consumos;
    }

    public String getConsumoMensal() {
        return consumoMensal;
    }

    public void setConsumoMensal(String consumoMensal) {
        this.consumoMensal = consumoMensal;
    }

    public String getMensagem() {
        return mensagem;
    }

    public void setMensagem(String mensagem) {
        this.mensagem = mensagem;
    }
}
