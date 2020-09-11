package com.testobject.httprequest;

import android.app.AlertDialog;
import android.app.DatePickerDialog;
import android.app.Dialog;
import android.content.DialogInterface;
import android.os.Bundle;
import android.widget.DatePicker;
import android.widget.TextView;

import androidx.fragment.app.DialogFragment;

import java.util.Calendar;

public class DatePickerFragment extends DialogFragment implements DatePickerDialog.OnDateSetListener{

    private String tipo;

    public DatePickerFragment(String tipo) {
        this.tipo = tipo;
    }

    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState){
        final Calendar calendar = Calendar.getInstance();
        int year = calendar.get(Calendar.YEAR);
        int month = calendar.get(Calendar.MONTH);
        int day = calendar.get(Calendar.DAY_OF_MONTH);

        DatePickerDialog datepickerdialog = new DatePickerDialog(getActivity(),
                AlertDialog.THEME_HOLO_LIGHT,this,year,month,day);

        datepickerdialog.setCancelable(false);

        return datepickerdialog;
    }


    @Override
    public void onDateSet(DatePicker view, int year, int month, int dayOfMonth) {
        TextView textview = getActivity().findViewById(R.id.txt_data);

        if(this.tipo.equals("diario")) {
            textview.setText(String.format("%02d/%02d/%04d", dayOfMonth, (month + 1), year));
        }
        else if(this.tipo.equals("mensal")){
            textview.setText(String.format("%02d/%04d", (month + 1), year));
        }
        else if(this.tipo.equals("anual")){
            textview.setText(String.format("%04d", year));
        }

    }

}
