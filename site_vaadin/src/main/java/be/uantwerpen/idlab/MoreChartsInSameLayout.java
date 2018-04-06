package be.uantwerpen.idlab; /**
 * Copyright (C) 2012-2013  Dušan Vejnovič  <vaadin@dussan.org>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import com.vaadin.ui.Label;
import com.vaadin.ui.VerticalLayout;
import org.dussan.vaadin.dcharts.DCharts;
import org.dussan.vaadin.dcharts.base.elements.XYaxis;
import org.dussan.vaadin.dcharts.data.DataSeries;
import org.dussan.vaadin.dcharts.data.Ticks;
import org.dussan.vaadin.dcharts.events.click.ChartDataClickEvent;
import org.dussan.vaadin.dcharts.events.click.ChartDataClickHandler;
import org.dussan.vaadin.dcharts.events.mouseenter.ChartDataMouseEnterEvent;
import org.dussan.vaadin.dcharts.events.mouseenter.ChartDataMouseEnterHandler;
import org.dussan.vaadin.dcharts.events.mouseleave.ChartDataMouseLeaveEvent;
import org.dussan.vaadin.dcharts.events.mouseleave.ChartDataMouseLeaveHandler;
import org.dussan.vaadin.dcharts.events.rightclick.ChartDataRightClickEvent;
import org.dussan.vaadin.dcharts.events.rightclick.ChartDataRightClickHandler;
import org.dussan.vaadin.dcharts.metadata.renderers.AxisRenderers;
import org.dussan.vaadin.dcharts.metadata.renderers.SeriesRenderers;
import org.dussan.vaadin.dcharts.options.Axes;
import org.dussan.vaadin.dcharts.options.Highlighter;
import org.dussan.vaadin.dcharts.options.Options;
import org.dussan.vaadin.dcharts.options.SeriesDefaults;
import org.dussan.vaadin.dcharts.renderers.series.PieRenderer;

import com.vaadin.ui.HorizontalLayout;

public class MoreChartsInSameLayout extends VerticalLayout {

    @Override
    public void attach() {
        super.attach();
        init();
    }

    public void init() {
        DCharts demo1 = DemoChart1();
        DCharts demo2 = DemoChart2();
        DCharts demo3 = DemoChart3();

        HorizontalLayout layout = new HorizontalLayout();
        layout.setSpacing(true);
        layout.setWidth("930px");
        layout.addComponent(demo1);
        layout.addComponent(demo2);
        layout.addComponent(demo3);
        addComponent(layout);
        addComponent(new Label("a label"));

        //setJqPlotCode(null);
        //setDChatsCode(null);
    }

    private DCharts DemoChart1() {
        DataSeries dataSeries = new DataSeries().add(2, 6, 7, 10);

        SeriesDefaults seriesDefaults = new SeriesDefaults()
                .setRenderer(SeriesRenderers.BAR);

        Axes axes = new Axes().addAxis(new XYaxis().setRenderer(
                AxisRenderers.CATEGORY).setTicks(
                new Ticks().add("a", "b", "c", "d")));

        Highlighter highlighter = new Highlighter().setShow(false);

        Options options = new Options().setCaptureRightClick(true)
                .setSeriesDefaults(seriesDefaults).setAxes(axes)
                .setHighlighter(highlighter);

        DCharts chart = new DCharts();
        chart.setWidth(300, Unit.PIXELS);
        chart.setHeight(300, Unit.PIXELS);
        chart.setDataSeries(dataSeries).setOptions(options);

        chart.setEnableChartDataMouseEnterEvent(true);
        chart.setEnableChartDataMouseLeaveEvent(true);
        chart.setEnableChartDataClickEvent(true);
        chart.setEnableChartDataRightClickEvent(true);

//        chart.addHandler(new ChartDataMouseEnterHandler() {
//            @Override
//            public void onChartDataMouseEnter(ChartDataMouseEnterEvent event) {
//                showNotification("CHART DATA MOUSE ENTER", event.getChartData());
//            }
//        });
//
//        chart.addHandler(new ChartDataMouseLeaveHandler() {
//            @Override
//            public void onChartDataMouseLeave(ChartDataMouseLeaveEvent event) {
//                showNotification("CHART DATA MOUSE LEAVE", event.getChartData());
//            }
//        });
//
//        chart.addHandler(new ChartDataClickHandler() {
//            @Override
//            public void onChartDataClick(ChartDataClickEvent event) {
//                showNotification("CHART DATA CLICK", event.getChartData());
//            }
//        });
//
//        chart.addHandler(new ChartDataRightClickHandler() {
//            @Override
//            public void onChartDataRightClick(ChartDataRightClickEvent event) {
//                showNotification("CHART DATA RIGHT CLICK", event.getChartData());
//            }
//        });

        chart.show();
        return chart;
    }

    private DCharts DemoChart2() {
        DataSeries dataSeries = new DataSeries().newSeries().add("none", 23)
                .add("error", 0).add("click", 5).add("impression", 25);

        SeriesDefaults seriesDefaults = new SeriesDefaults().setRenderer(
                SeriesRenderers.PIE).setRendererOptions(
                new PieRenderer().setShowDataLabels(true));

        Options options = new Options().setCaptureRightClick(true)
                .setSeriesDefaults(seriesDefaults);

        DCharts chart = new DCharts();
        chart.setWidth(300, Unit.PIXELS);
        chart.setHeight(300, Unit.PIXELS);
        chart.setDataSeries(dataSeries).setOptions(options);

        chart.setEnableChartDataMouseEnterEvent(true);
        chart.setEnableChartDataMouseLeaveEvent(true);
        chart.setEnableChartDataClickEvent(true);
        chart.setEnableChartDataRightClickEvent(true);

//        chart.addHandler(new ChartDataMouseEnterHandler() {
//            @Override
//            public void onChartDataMouseEnter(ChartDataMouseEnterEvent event) {
//                showNotification("CHART DATA MOUSE ENTER", event.getChartData());
//            }
//        });
//
//        chart.addHandler(new ChartDataMouseLeaveHandler() {
//            @Override
//            public void onChartDataMouseLeave(ChartDataMouseLeaveEvent event) {
//                showNotification("CHART DATA MOUSE LEAVE", event.getChartData());
//            }
//        });
//
//        chart.addHandler(new ChartDataClickHandler() {
//            @Override
//            public void onChartDataClick(ChartDataClickEvent event) {
//                showNotification("CHART DATA CLICK", event.getChartData());
//            }
//        });
//
//        chart.addHandler(new ChartDataRightClickHandler() {
//            @Override
//            public void onChartDataRightClick(ChartDataRightClickEvent event) {
//                showNotification("CHART DATA RIGHT CLICK", event.getChartData());
//            }
//        });

        chart.show();
        return chart;
    }

    private DCharts DemoChart3() {
        DataSeries dataSeries = new DataSeries().newSeries().add("none", 23)
                .add("error", 0).add("click", 5).add("impression", 25);

        SeriesDefaults seriesDefaults = new SeriesDefaults().setRenderer(
                SeriesRenderers.PIE).setRendererOptions(
                new PieRenderer().setFill(false).setShowDataLabels(true));

        Options options = new Options().setCaptureRightClick(true)
                .setSeriesDefaults(seriesDefaults);

        DCharts chart = new DCharts();
        chart.setWidth(300, Unit.PIXELS);
        chart.setHeight(300, Unit.PIXELS);
        chart.setDataSeries(dataSeries).setOptions(options);

        chart.setEnableChartDataMouseEnterEvent(true);
        chart.setEnableChartDataMouseLeaveEvent(true);
        chart.setEnableChartDataClickEvent(true);
        chart.setEnableChartDataRightClickEvent(true);

//        chart.addHandler(new ChartDataMouseEnterHandler() {
//            @Override
//            public void onChartDataMouseEnter(ChartDataMouseEnterEvent event) {
//                showNotification("CHART DATA MOUSE ENTER", event.getChartData());
//            }
//        });
//
//        chart.addHandler(new ChartDataMouseLeaveHandler() {
//            @Override
//            public void onChartDataMouseLeave(ChartDataMouseLeaveEvent event) {
//                showNotification("CHART DATA MOUSE LEAVE", event.getChartData());
//            }
//        });
//
//        chart.addHandler(new ChartDataClickHandler() {
//            @Override
//            public void onChartDataClick(ChartDataClickEvent event) {
//                showNotification("CHART DATA CLICK", event.getChartData());
//            }
//        });
//
//        chart.addHandler(new ChartDataRightClickHandler() {
//            @Override
//            public void onChartDataRightClick(ChartDataRightClickEvent event) {
//                showNotification("CHART DATA RIGHT CLICK", event.getChartData());
//            }
//        });

        chart.show();
        return chart;
    }

}
