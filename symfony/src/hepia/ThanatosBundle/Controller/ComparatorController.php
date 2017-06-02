<?php

namespace hepia\ThanatosBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;
use Symfony\Bridge\Doctrine\Form\Type\EntityType;
use Symfony\Component\HttpFoundation\Request;

class ComparatorController extends Controller {

    public function indexAction(Request $request) {
        $tData = array();
        $instances = array();

        $form = $this->createFormBuilder()
                ->setAction($this->generateUrl('hepia_thanatos_comparator'))
                ->add('instances', EntityType::class, array(
                    'class' => 'hepiaThanatosBundle:Instance',
                    'choice_label' => 'title',
                    'multiple' => true,))
                ->add('send', SubmitType::class)
                ->getForm();

        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $em = $this->getDoctrine()->getManager();
            $data = $form->getData();

            $counts = array();

            foreach ($data["instances"] as $instance) {
                $count = $this->getDoctrine()->getRepository('hepiaThanatosBundle:Validation')->countPublishedTotal($instance->getId());
                array_push($counts, $count);
            }

            $min = min($counts);
            $sum = array();

            foreach ($data["instances"] as $instance) {
                $array = array();
                $validations = $em
                        ->getRepository('hepiaThanatosBundle:Validation')
                        ->findBy(array('instance' => $instance), NULL, $min);
                $id = 0;
                foreach ($validations as $validation) {
                    array_push($array, [$validation->getAccuracy(), $validation->getValidation(), $validation->getTraining()]);
                    if (isset($sum[$id])) {
                        $sum[$id][0] = ($sum[$id][0] + $validation->getAccuracy()) / 2;
                        $sum[$id][1] = ($sum[$id][1] + $validation->getValidation()) / 2;
                        $sum[$id][2] = ($sum[$id][2] + $validation->getTraining()) / 2;
                    } else {
                        $sum[$id] = [$validation->getAccuracy(), $validation->getValidation(), $validation->getTraining()];
                    }
                    $id++;
                }
                if (count($array) > 0) {
                    array_push($instances, ["title" => $instance->getTitle(), "max" => max($array), "id" => $instance->getId()]);
                } else {
                    array_push($instances, ["title" => $instance->getTitle(), "max" => array(0), "id" => $instance->getId()]);
                }
                array_push($tData, [$array, $instance->getTitle()]);
            }

            array_push($tData, [$sum, "moyenne"]);
        }

        $this->get('hepia.js_vars')->tData = $tData;

        return $this->render('hepiaThanatosBundle:Comparator:index.html.twig', array("instances" => $instances));
    }

}
