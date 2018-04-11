package be.uantwerpen.idlab;

import javax.servlet.annotation.WebServlet;

import com.byteowls.vaadin.chartjs.ChartJs;
import com.byteowls.vaadin.chartjs.config.LineChartConfig;
import com.byteowls.vaadin.chartjs.data.LineDataset;
import com.byteowls.vaadin.chartjs.options.scale.Axis;
import com.byteowls.vaadin.chartjs.options.scale.CategoryScale;
import com.byteowls.vaadin.chartjs.options.scale.LinearScale;
import com.byteowls.vaadin.chartjs.utils.ColorUtils;
import com.vaadin.annotations.Theme;
import com.vaadin.annotations.VaadinServletConfiguration;
import com.vaadin.data.HasValue;
import com.vaadin.event.selection.SingleSelectionListener;
import com.vaadin.server.VaadinRequest;
import com.vaadin.server.Page;
import com.vaadin.server.VaadinServlet;
import com.vaadin.ui.*;
import com.vaadin.ui.themes.ValoTheme;
//import org.dussan.vaadin.dcharts.DCharts;
//import org.dussan.vaadin.dcharts.base.elements.XYaxis;
//import org.dussan.vaadin.dcharts.base.renderers.SeriesRenderer;
//import org.dussan.vaadin.dcharts.data.DataSeries;
//import org.dussan.vaadin.dcharts.data.Ticks;
//import org.dussan.vaadin.dcharts.defaults.renderers.series.DefaultLineRenderer;
//import org.dussan.vaadin.dcharts.metadata.LegendPlacements;
//import org.dussan.vaadin.dcharts.metadata.XYaxes;
//import org.dussan.vaadin.dcharts.metadata.locations.LegendLocations;
//import org.dussan.vaadin.dcharts.metadata.renderers.AxisRenderers;
//import org.dussan.vaadin.dcharts.metadata.renderers.LabelRenderers;
//import org.dussan.vaadin.dcharts.metadata.renderers.LegendRenderers;
//import org.dussan.vaadin.dcharts.metadata.renderers.SeriesRenderers;
//import org.dussan.vaadin.dcharts.metadata.ticks.TickFormatters;
//import org.dussan.vaadin.dcharts.options.*;
//import org.dussan.vaadin.dcharts.options.Grid;
//import org.dussan.vaadin.dcharts.renderers.legend.EnhancedLegendRenderer;
//import org.dussan.vaadin.dcharts.renderers.series.LineRenderer;
//import org.dussan.vaadin.dcharts.renderers.tick.CanvasAxisTickRenderer;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import time;
import datetime;

/**
 * This UI is the application entry point. A UI may either represent a browser window 
 * (or tab) or some part of an HTML page where a Vaadin application is embedded.
 * <p>
 * The UI is initialized using {@link #init(VaadinRequest)}. This method is intended to be 
 * overridden to add component to the user interface and initialize non-component functionality.
 */
@Theme("mytheme")
public class MyUI extends UI {

    private static final Path directory = Paths.get("/home/jstruye/citylab-interference-demo");
    private static final  String LONGRANGE = "24 hours";
    private static final String SHORTRANGE = "30 minutes";

    private static final int MEASURE_INTERVAL = 6;
    private static final int PREDICT_RANGE = 100;

    private static final Double CHART_PREDICT_WIDTH = 10.0d;

    private String node = null;
    private String freq = null;
    private String windowRange = null;

    private Component chartComponent = null;
    private Label mostRecent = null;



    @Override
    protected void init(VaadinRequest vaadinRequest) {
        boolean isMobile = false;
        String frag = Page.getCurrent().getUriFragment();
        if (frag != null && frag.equals("mobile")) {
            isMobile = true;
        }
        final VerticalLayout layout = new VerticalLayout();


        final TextField name = new TextField();
        name.setCaption("Type your name here:");

        Button button = new Button("Click Me");
        button.addClickListener(e -> {
            layout.addComponent(new Label("Thanks " + name.getValue() 
                    + ", it works!"));
        });

        final ComboBox nodeBox = new ComboBox();
        List<String> nodes = new ArrayList<>();
        if (!isMobile) {
            try {
                Files.readAllLines(Paths.get(directory.toString(), "nodes")).forEach(line-> {nodes.add(line);});
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        else {
            nodes.add("67");
        }
        nodeBox.setItems(nodes);
        if (isMobile) {
            node = "67";
        }
        nodeBox.setVisible(!isMobile);

        nodeBox.addValueChangeListener((HasValue.ValueChangeListener) valueChangeEvent -> {
            Object value = valueChangeEvent.getValue();
            if (value != null) {
                node = value.toString();
            } else {
                node = null;
            }
            buildChart(layout);
        });

        final ComboBox freqBox = new ComboBox();
        List<String> freqs = new ArrayList<>();
        try {
            Files.readAllLines(Paths.get(directory.toString(), "freqs")).forEach(line-> {freqs.add(line);});
        } catch (IOException e) {
            e.printStackTrace();
        }
        freqBox.setItems(freqs);
        freqBox.addValueChangeListener((HasValue.ValueChangeListener) valueChangeEvent -> {
            Object value = valueChangeEvent.getValue();
            if (value != null) {
                freq = value.toString();
            } else {
                freq = null;
            }
            buildChart(layout);
        });

        RadioButtonGroup<String> windowGroup = new RadioButtonGroup<>();
        windowGroup.addStyleName(ValoTheme.OPTIONGROUP_HORIZONTAL);
        windowGroup.setItems(LONGRANGE, SHORTRANGE);
        windowGroup.addSelectionListener((SingleSelectionListener<String>) singleSelectionEvent -> {
            windowRange = singleSelectionEvent.getValue();
            buildChart(layout);
        });
        windowGroup.setSelectedItem(LONGRANGE);


        HorizontalLayout options = new HorizontalLayout();
        options.addComponent(nodeBox);
        options.addComponent(freqBox);
        options.addComponent(windowGroup);
        options.setDefaultComponentAlignment(Alignment.MIDDLE_LEFT);
        options.setSizeUndefined();
        layout.addComponent(options);
        //layout.addComponents(name, button);

        setContent(layout);

        System.out.println(System.getProperty("java.class.path"));

//        DataSeries dataSeries = new DataSeries()
//                //.add(0.9176, 0.9296, 0.927, 0.9251, 0.9241, 0.9225, 0.9197, 0.9164, 0.9131, 0.9098, 0.9064, 0.9028, 0.8991, 0.8957, 0.8925, 0.8896, 0.8869, 0.8844, 0.882, 0.8797, 0.8776, 0.8755, 0.8735, 0.8715, 0.8696, 0.8677, 0.8658, 0.8637, 0.8616, 0.8594, 0.8572, 0.8548, 0.8524, 0.8499, 0.8473, 0.8446, 0.8418, 0.8389, 0.8359, 0.8328, 0.8295, 0.8262, 0.8227, 0.8191, 0.8155, 0.8119, 0.8083, 0.8048, 0.8013, 0.7979, 0.7945, 0.7912, 0.7879, 0.7846, 0.7813, 0.778, 0.7747, 0.7714, 0.768, 0.7647, 0.7612, 0.7577, 0.7538, 0.7496, 0.7449, 0.7398, 0.7342, 0.7279, 0.721, 0.7137, 0.7059, 0.6977, 0.6889, 0.6797, 0.6698, 0.6593, 0.6482, 0.6367, 0.6247, 0.6121, 0.5989, 0.5852, 0.571, 0.5561, 0.5402, 0.5232, 0.505, 0.4855, 0.4643, 0.4414, 0.4166, 0.3893, 0.3577, 0.3204, 0.2764, 0.2272, 0.1774, 0.1231, 0.0855, 0.0849);
//                .add(1,5,4,7,3,2,1,2,5,6,4)
//                .add(1,1,1,1,1,1,1,1,1,1,1);
//
//        DataSeries dataSeries2 = new DataSeries()
//                .add(1,3,1,3,1,3,1,3,1,3,1,3)
//                .add(1,3,1,3,1,3,1,3,1,3,1,3);
//
//
//
//        Title title = new Title("Contribution of Urban and Rural Population to National Percentiles (edited data)");
//
//        LineRenderer rend = new LineRenderer();
//        rend.setHighlightMouseOver(false);
//        SeriesDefaults seriesDefaults = new SeriesDefaults()
//        .setShowMarker(false)
//                .setShadow(false)
//            .setRendererOptions(rend)
//        .setFill(true)
//        .setFillAndStroke(false);
//
//
//        Legend legend = new Legend()
//        .setShow(true)
//        .setRenderer(LegendRenderers.ENHANCED)
//        .setRendererOptions(
//                new EnhancedLegendRenderer()
//                        .setNumberRows(1))
//        .setPlacement(LegendPlacements.OUTSIDE_GRID)
//        .setLabels("Rural", "Urban")
//        .setLocation(LegendLocations.SOUTH);
//
////        Axes axes = new Axes()
////                .addAxis(
////                        new XYaxis(XYaxes.X)
////                        .setPad(0)
////                        .setMin(1)
////                        .setMax(100)
////                        .setLabel("Population Percentile")
////                        .setLabelRenderer(LabelRenderers.CANVAS)
////                        .setTickInterval(3)
////                        .setTickOptions(
////                                new CanvasAxisTickRenderer()
////                                        .setShowGridline(true)))
////                .addAxis(
////                        new XYaxis(XYaxes.Y)
////                        .setMin(0)
////                        .setMax(1)
////                        .setLabel("Percentage of Population")
////                        .setLabelRenderer(LabelRenderers.CANVAS)
////                        .setTickOptions(
////                                new CanvasAxisTickRenderer()
////                                        .setFormatter(TickFormatters.PERCENT)
////                                        .setShowGridline(true)
////                                        .setFormatString("%d%%")));
//
//        Grid grid = new Grid()
//        //.setDrawBorder(true)
//        .setShadow(false);
//        //.setBackground("white");
//
//        CanvasOverlay overlay = new CanvasOverlay();
//        Options options = new Options()
//                .setTitle(title)
//                .setStackSeries(true)
//                .setSeriesColors("rgba(255, 255, 255, 0.0)", "#B9CDE5")
//                .setSeriesDefaults(seriesDefaults)
//                .setLegend(legend)
//                //.setAxes(axes);
//                //.setCanvasOverlay(new CanvasOverlay())
//                .setGrid(grid);
//
//        DCharts chart = new DCharts()
//                .setDataSeries(dataSeries)
//                .setOptions(options)
//                .setEnableChartImageChangeEvent(true)
//                .show();
//        chart.setDataSeries(dataSeries2).show();


        //layout.addComponent(chart);
        this.chartComponent = new VerticalLayout();
        this.chartComponent.setSizeFull();
        layout.addComponent(this.chartComponent);
        layout.setExpandRatio(this.chartComponent, 1.0f);

	mostRecent = new Label();
        layout.addComponent(mostRecent);
        layout.setComponentAlignment(mostRecent, Alignment.BOTTOM_RIGHT);
        layout.setSizeFull();
        layout.setHeight("800px");
        this.setSizeFull();

    }

    private void buildChart(VerticalLayout layout) {
        if (node == null || freq == null) {
            return;
        }


        // generate data
        List<Double> data = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(Paths.get(directory.toString(), "../predicted/" + node + "/" + freq + ".out").toString()))) {
            String line;

            while ((line = br.readLine()) != null) {
                String[] splits = line.split(",");
                if (splits.length < 2) {
                    break;
                }
                data.add(new Double(splits[1]) - (CHART_PREDICT_WIDTH / 2.0));
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }



        // generate data
        List<Double> data2 = new ArrayList<>(data);
        for (int i = 0; i < data2.size(); i++) {
            data2.set(i, data2.get(i) + CHART_PREDICT_WIDTH);
        }

        // generate data
        String mostRecentDate = null;
        List<Double> data3 = new ArrayList<>();
        List<Double> timestamps = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(Paths.get(directory.toString(), "../smoothed/" + node + "/" + freq + ".out").toString()))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] splits = line.split(",");
                if (splits.length < 2) {
                    break;
                }
                data3.add(new Double(splits[1]));
                double date = time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple());
                timestamps.append(date);
                mostRecentDate = splits[0];
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        if (mostRecentDate != null) {
            mostRecent.setValue("Most recent date: " + mostRecentDate.toString());
        }

        List<String> zeroLabels = new ArrayList<>();
        for (date : timestamps) {
            zeroLabels.add(new Double(date).toString());
        }

        String windowMin;
        String windowMax;
        switch(this.windowRange) {
            case LONGRANGE:
                //24h
                double startPoint = timestamps.get(timestamps.size() - 1) - (24*60*60);
                int skips = 0;
                for (date : timestamps) {
                    if (date < startPoint) {
                        skips++;
                    } else {
                        break;
                    }
                }
                windowMin = zeroLabels.get(skips);
                windowMax = zeroLabels.get(zeroLabels.size() - 1);
                break;
            case SHORTRANGE:
                //30min
                double startPoint = timestamps.get(timestamps.size() - 1) - (30*60);
                int skips = 0;
                for (date : timestamps) {
                    if (date < startPoint) {
                        skips++;
                    } else {
                        break;
                    }
                }
                windowMin = zeroLabels.get(skips);
                windowMax = zeroLabels.get(zeroLabels.size() - 1);
                break;
            default:
                windowMin = zeroLabels.get(0);
                windowMax = zeroLabels.get(zeroLabels.size() - 1);
                break;

        }
        LineChartConfig config = new LineChartConfig();
        config
                .data()
                //.labels("January", "February", "March", "April", "May", "June", "July", "August")
                .labels(zeroLabels.toArray(new String[]{}))
                //.addDataset(new LineDataset().hidden(true))
                .addDataset(new LineDataset().fill(false, 0))
                //.addDataset(new LineDataset().hidden(true).fill(1))
                .addDataset(new LineDataset().fill(true, 1))
                .addDataset(new LineDataset().fill(false, 0))
                //.addDataset(new LineDataset().fill(false, 1))
                //.addDataset(new LineDataset().fill(true, 2))
                //.addDataset(new LineDataset().fill(false))
                //.addDataset(new LineDataset().fill(8))
                //.addDataset(new LineDataset().hidden(true).fill(FillMode.END))
                .and();

        config.
                options()
                .maintainAspectRatio(false)
                .elements()
                .line()
                .tension(0.00001d)
                .and()
                .and()
                .scales()
                .add(Axis.Y, new LinearScale().stacked(false))
                .and()
                .scales()
                .add(Axis.X, new CategoryScale()
                        .ticks().min(windowMin).max(windowMax).and()
                    .display(false)
                    .scaleLabel()
                    .display(false)
                    .and())
                .and()
                .title()
                .display(true)
                //.text("Advanced line fill options")
                .and()
                .done();

        LineDataset lds = (LineDataset) config.data().getDatasetAtIndex(2);
        lds.label("D"+0);
        int[] rgb = DemoUtils.getRgbColor(2);
        lds.borderColor(ColorUtils.toRgb(rgb));
        lds.backgroundColor(ColorUtils.toRgba(rgb, 0.5));
        lds.dataAsList(data);

        LineDataset lds2 = (LineDataset) config.data().getDatasetAtIndex(1);
        lds2.label("D"+1);
        int[] rgb2 = DemoUtils.getRgbColor(2);
        lds2.borderColor(ColorUtils.toRgb(rgb2));
        lds2.backgroundColor(ColorUtils.toRgba(rgb2, 0.5));
        lds2.dataAsList(data2);

        LineDataset lds3 = (LineDataset) config.data().getDatasetAtIndex(0);
        lds3.label("D"+2);
        int[] rgb3 = DemoUtils.getRgbColor(1);
        lds3.borderColor(ColorUtils.toRgb(rgb3));
        lds3.backgroundColor(ColorUtils.toRgba(rgb3, 1.0));
        lds3.dataAsList(data3);


        //SampleDataConfig sampleConfig =
        //        new SampleDataConfig().min(20).max(80).count(8).decimals(2).continuity(1);
        //for (int i = 0; i < config.data().getDatasets().size(); i++) {



        //}

        ChartJs chart = new ChartJs(config);
        chart.setJsLoggingEnabled(true);

        chart.addClickListener((a,b) ->
                DemoUtils.notification(a, b, config.data().getDatasets().get(a)));
        chart.setSizeFull();

        layout.replaceComponent(chartComponent, chart);
        this.chartComponent = chart;
        layout.setExpandRatio(chart, 1.0f);
    }

    @WebServlet(urlPatterns = "/*", name = "MyUIServlet", asyncSupported = true)
    @VaadinServletConfiguration(ui = MyUI.class, productionMode = false)
    public static class MyUIServlet extends VaadinServlet {
    }
}

