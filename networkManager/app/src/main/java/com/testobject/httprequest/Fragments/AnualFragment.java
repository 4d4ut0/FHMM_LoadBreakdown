package com.testobject.httprequest.Fragments;

import android.app.AlertDialog;
import android.app.DatePickerDialog;
import android.app.ProgressDialog;
import android.content.Context;
import android.graphics.Color;
import android.os.Bundle;

import androidx.fragment.app.DialogFragment;
import androidx.fragment.app.Fragment;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.inputmethod.InputMethodManager;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.TextView;

import com.google.common.io.ByteStreams;
import com.google.gson.Gson;
import com.jjoe64.graphview.DefaultLabelFormatter;
import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.BarGraphSeries;
import com.jjoe64.graphview.series.DataPoint;
import com.testobject.httprequest.DatePickerFragment;
import com.testobject.httprequest.R;
import com.testobject.httprequest.respConsumo.Consumo;
import com.testobject.httprequest.respConsumo.respConsumo;
import com.testobject.httprequest.respDevice.Device;

import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link AnualFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class AnualFragment extends Fragment {
    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";
    private static final String ARG_PARAM3 = "param3";
    private static final String ARG_PARAM4 = "param4";
    // TODO: Rename and change types of parameters
    private String userName;
    private String userId;
    private String estacaoId = "1345";
    private String estacaoName;
    private String urlInicial = "http://nexsolar.sytes.net/ceb/api/consumo/";
    private String api = "/anual/";
    private String urlDevice = "http://nexsolar.sytes.net/ceb/api/estacao/usuario/";
    private Device[] deviceList;
    private ArrayList<Consumo> respsConsumos;
    private ArrayList<Date> x;
    private ArrayList<Float> y;
    private ProgressDialog progressDialog;
    private View rootView;
    private GraphView graph;
    private AutoCompleteTextView acTxtTipo;
    private TextView txtData;
    private Button btnGenerate;
    public AnualFragment() {
        // Required empty public constructor
    }

    // TODO: Rename and change types and number of parameters
    public static AnualFragment newInstance(String param1, String param2, String param3, String param4) {
        AnualFragment fragment = new AnualFragment();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, param1);
        args.putString(ARG_PARAM2, param2);
        args.putString(ARG_PARAM3, param3);
        args.putString(ARG_PARAM4, param4);
        fragment.setArguments(args);
        return fragment;
    }
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            userName = getArguments().getString(ARG_PARAM1);
            userId = getArguments().getString(ARG_PARAM2);
            estacaoId = getArguments().getString(ARG_PARAM3);
            estacaoName = getArguments().getString(ARG_PARAM4);
        }
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        declaration(inflater, container);

        InputMethodManager in = (InputMethodManager) getActivity().getSystemService(Context.INPUT_METHOD_SERVICE);

        acTxtTipo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                in.hideSoftInputFromWindow(getView().getWindowToken(), 0);
                acTxtTipo.showDropDown();
            }
        });

        acTxtTipo.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                in.hideSoftInputFromWindow(getView().getWindowToken(), 0);
                acTxtTipo.showDropDown();
            }
        });

        txtData.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                DialogFragment dialogfragment = new DatePickerFragment("anual");
                dialogfragment.setCancelable(false);
                dialogfragment.show(getFragmentManager(), "Theme 3");
            }
        });

        btnGenerate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                generatGraph();
            }
        });

        return rootView;
    }

    public Device[] getDevices(){
        try {
            final java.net.URL url = new URL(urlDevice + userId);
            final HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.connect();

            final InputStream stream = connection.getInputStream();
            String oloco = new String(ByteStreams.toByteArray(stream));
            Device[] msg = new Gson().fromJson(oloco, Device[].class);
            return msg;
        } catch (Exception e) {
            Log.e("Your tag", "Error", e);
        }
        return null;
    }

    public ArrayList<Consumo> getConsumo(String estacaoId, String data){
        try {
            final java.net.URL url = new URL(urlInicial + estacaoId + api + data);
            final HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.connect();

            final InputStream stream = connection.getInputStream();
            String oloco = new String(ByteStreams.toByteArray(stream));
            Log.v("oloco", oloco);
            respConsumo msg = new Gson().fromJson(oloco, respConsumo.class);
            if (msg == null) return null;
            else return sortByDate(msg.getConsumos());
        } catch (Exception e){
            Log.e("Your tag", "Error", e);
        }
        return null;
    }

    public ArrayList<Date> findDataConsumo (){
        ArrayList<Date> resp = new ArrayList<>();
        for (Consumo consumo: respsConsumos) {
            resp.add(convertStringToDate(consumo.getDataTimeInsere()));
        }

        return resp;
    }

    public ArrayList<Float> findPotenciaConsumo (){
        ArrayList<Float> resp = new ArrayList<>();
        for (Consumo consumo: respsConsumos)
            resp.add(consumo.getPotencia()/1000)  ;

        return resp;
    }

    public void startDialog(String title, String msg){
        progressDialog = new ProgressDialog(getContext());
        progressDialog.setIndeterminate(true);
        progressDialog.setTitle(title);
        progressDialog.setMessage(msg);
        progressDialog.setCanceledOnTouchOutside(false);
        progressDialog.setMax(100);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.show();
    }

    public void generatGraph(){
        startDialog("Buscando dados de consumo", "Tiruriruriruruuuu, rururu, rurururuuuuu");
        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                try  {
                    Log.v("teste", findIdbyName(acTxtTipo.getText().toString()));
                    respsConsumos = getConsumo(findIdbyName(acTxtTipo.getText().toString()),txtData.getText().toString());

                    if(respsConsumos != null) {
                        y = findPotenciaConsumo();
                        x = findDataConsumo();

                        DataPoint[] data = new DataPoint[y.size()];
                        for (int i = 0; i < data.length; i++) {
                            data[i] = new DataPoint(x.get(i), y.get(i));
                        }

                        BarGraphSeries<DataPoint> series = new BarGraphSeries<DataPoint>(data);


                        graph.addSeries(series);
                        series.setSpacing(100);
                        series.setDrawValuesOnTop(true);
                        series.setValuesOnTopColor(Color.RED);
                        Calendar mCalendar = Calendar.getInstance();
                        SimpleDateFormat mDateFormat = new SimpleDateFormat("MM");
                        graph.getGridLabelRenderer().setLabelFormatter(new DefaultLabelFormatter() {
                            @Override
                            public String formatLabel(double value, boolean isValueX) {
                                if (isValueX) {
                                    mCalendar.setTimeInMillis((long) value);
                                    System.out.println(mDateFormat.format(mCalendar.getTimeInMillis()));
                                    return mDateFormat.format(mCalendar.getTimeInMillis());
                                } else {
                                    return super.formatLabel(value, isValueX);
                                }
                            }
                        });


                    }

                    progressDialog.dismiss();

                } catch (Exception e) {
                    Log.e("iririr", "Erro no parsing do JSON", e);
                }
            }
        });
        thread.start();
    }

    public Date convertStringToDate(String dtStart){
        SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
        try {
            Date date = format.parse(dtStart);
            return date;
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return  null;
    }

    public ArrayList<Consumo> sortByDate(ArrayList<Consumo> consumos){
        Consumo aux;
        for(int i = 0; i < consumos.size(); i++)
            for(int j = 0; j < consumos.size(); j++){
                if(consumos.get(i).compareTo(consumos.get(j)) < 0){
                    aux = consumos.get(j);
                    consumos.set(j, consumos.get(i));
                    consumos.set(i, aux);
                }
            }
        return consumos;
    }

    public String [] deviceNameList(){
        String[] resp = new String[deviceList.length];
        for (int i = 0; i< resp.length; i++) {
            resp[i] = deviceList[i].getApelido();
            Log.v(Integer.toString(i), resp[i]);
        }
        return resp;
    }

    public String findIdbyName(String name){
        String last = "-1";
        for(Device device: deviceList){
            if(device.getApelido().equals(name))last = device.getIdEstacao().toString();
        }
        return last;
    }

    public void declaration(LayoutInflater inflater, ViewGroup container){
        rootView = inflater.inflate(R.layout.fragment_diario, container, false);
        graph = rootView.findViewById(R.id.graph);
        txtData = rootView.findViewById(R.id.txt_data);
        acTxtTipo = rootView.findViewById(R.id.txt_id_dv);
        btnGenerate = rootView.findViewById(R.id.button_generate);

        final Calendar calendar = Calendar.getInstance();
        int year = calendar.get(Calendar.YEAR);
        int month = calendar.get(Calendar.MONTH);
        int day = calendar.get(Calendar.DAY_OF_MONTH);
        txtData.setText(Integer.toString(year));
        //txtData.setText("2011");
        acTxtTipo.setText(estacaoName);

        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                try  {
                    deviceList = getDevices();
                    ArrayAdapter<String> adapter = new ArrayAdapter<String>(getActivity(), android.R.layout.simple_list_item_1, deviceNameList());

                    getActivity().runOnUiThread(new Runnable() {
                        public void run() {
                            acTxtTipo.setAdapter(adapter);
                            //acTxtTipo.setText(deviceList[0].getApelido());
                        }
                    });

                } catch (Exception e) {
                    Log.e("iririr", "Erro no parsing do JSON", e);
                }
            }
        });
        thread.start();
    }

}
