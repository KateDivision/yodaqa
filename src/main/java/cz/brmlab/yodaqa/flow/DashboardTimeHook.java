package cz.brmlab.yodaqa.flow;

import java.util.ArrayList;
import java.util.List;
import java.util.Iterator;

import org.apache.uima.UimaContext;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.fit.component.JCasAnnotator_ImplBase;
import org.apache.uima.fit.descriptor.ConfigurationParameter;
import org.apache.uima.fit.util.JCasUtil;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceInitializationException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import cz.brmlab.yodaqa.flow.dashboard.*;
import cz.brmlab.yodaqa.model.Question.QuestionInfo;

/**
 * Time the question analysis results in the question dashboard.
 * This is used to report ongoing progress through user interfaces. */

public class DashboardTimeHook extends JCasAnnotator_ImplBase {
    final Logger logger = LoggerFactory.getLogger(DashboardTimeHook.class);

    // Index in the table of the timestamps
    public static final String INDEX = "INDEX";
    @ConfigurationParameter(name = INDEX, mandatory = true, defaultValue = "0")
    protected int index;

    public void initialize(UimaContext aContext) throws ResourceInitializationException {
        super.initialize(aContext);
    }

    public void process(JCas view) throws AnalysisEngineProcessException {
        String viewTextType = "";
        //boolean initViewSeen = false;
        boolean done = false;
        JCas workingView;
        try {
            Iterator<JCas> viewIt = view.getViewIterator();
            while (viewIt.hasNext() && !done) {
                workingView = viewIt.next();
                viewTextType = workingView.getViewName();
                //System.out.println("Found View " + viewTextType);
                if (viewTextType.equals("_InitialView") || viewTextType.equals("Question")){
                    //initViewSeen = true;
                    try {
                        QuestionInfo qi = JCasUtil.selectSingle(workingView, QuestionInfo.class);
                        QuestionDashboard.getInstance().get(qi.getQuestionId()).setTimestamp(this.index);
                        done = true;
                        //System.out.println("Found View " + viewTextType);
                    } catch (Exception e){}
                }
            }
            //System.out.println("Found View " + viewTextType);
        } catch (Exception e){
            throw new AnalysisEngineProcessException(e);
        }
        /*JCas workingView;
        try {
            //questionView = view.getView("Question");
            workingView = view.getView(viewTextType);
            //System.out.println("Found Question View");
            //QuestionInfo qi = JCasUtil.selectSingle(workingView, QuestionInfo.class);
            //QuestionDashboard.getInstance().get(qi.getQuestionId()).setTimestamp(this.index);
        } catch (Exception e) {
            throw new AnalysisEngineProcessException(e);
        }*/

    }
}
