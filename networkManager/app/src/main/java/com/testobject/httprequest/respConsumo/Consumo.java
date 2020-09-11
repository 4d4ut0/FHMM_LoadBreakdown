package com.testobject.httprequest.respConsumo;

import java.net.Inet4Address;
import java.util.ArrayList;

public class Consumo {
    private String idHardware;
    private String dataRegistro;
    private String dataTimeInsere;
    private Float potencia;
    private Float energiaConsumida;

    public String getIdHardware() {
        return idHardware;
    }

    public void setIdHardware(String idHardware) {
        this.idHardware = idHardware;
    }

    public String getDataRegistro() {
        return dataRegistro;
    }

    public void setDataRegistro(String dataRegistro) {
        this.dataRegistro = dataRegistro;
    }

    public String getDataTimeInsere() {
        return dataTimeInsere;
    }

    public void setDataTimeInsere(String dataTimeInsere) {
        this.dataTimeInsere = dataTimeInsere;
    }

    public Float getPotencia() {
        return potencia;
    }

    public void setPotencia(Float potencia) {
        this.potencia = potencia;
    }

    public Float getEnergiaConsumida() {
        return energiaConsumida;
    }

    public void setEnergiaConsumida(Float energiaConsumida) {
        this.energiaConsumida = energiaConsumida;
    }

    public int compareTo(Consumo outro){
        return this.getDataTimeInsere().compareTo(outro.getDataTimeInsere());
    }

    public String getDataSegundTimeInsere() {
        return dataTimeInsere.split("T")[1];
    }

}
