package com.testobject.httprequest.respHorimetroConsumo;

public class ConsumoHorimetro {
    private String tipo;
    private Integer idHorimetro;
    private Double tempoTotal;
    private String dataRegistro;

    public String getTipo() {
        return tipo;
    }

    public void setTipo(String tipo) {
        this.tipo = tipo;
    }

    public Integer getIdHorimetro() {
        return idHorimetro;
    }

    public void setIdHorimetro(Integer idHorimetro) {
        this.idHorimetro = idHorimetro;
    }

    public Double getTempoTotal() {
        return tempoTotal;
    }

    public void setTempoTotal(Double tempoTotal) {
        this.tempoTotal = tempoTotal;
    }

    public String getDataRegistro() {
        return dataRegistro;
    }

    public void setDataRegistro(String dataRegistro) {
        this.dataRegistro = dataRegistro;
    }
}
