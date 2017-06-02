<?php

namespace hepia\ThanatosBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\Extension\Core\Type\FormType;
use Symfony\Bridge\Doctrine\Form\Type\EntityType;
use Symfony\Component\HttpFoundation\Request;
use hepia\ThanatosBundle\Entity\Instance;
use Symfony\Component\Form\Extension\Core\Type\ChoiceType;

class InstanceController extends Controller {

    public function viewAction($id) {
        $em = $this->getDoctrine()->getManager();
        $instance = $this->getDoctrine()->getRepository('hepiaThanatosBundle:Instance')->getInstanceById($id);
        if (null === $instance) {
            throw new NotFoundHttpException("L'instance d'id " . $id . " n'existe pas.");
        }

        $tData = array();
        $saves = array();

        $computers = $this->container->get('hepia_thanatos.computer')->getAvailable();

        foreach (glob(__DIR__ . '/../../../../web/upload/save/' . $id . '/*.npz') as $value) {
            array_push($saves, ["name" => basename($value), "date" => gmdate("H:i:s d-m-Y", filectime($value) + 2 * 3600), "download" => 'upload/save/' . $id . '/' . basename($value)]);
        }

        $validations = $em
                ->getRepository('hepiaThanatosBundle:Validation')
                ->findBy(array('instance' => $instance));

        foreach ($validations as $validation) {
            array_push($tData, [$validation->getAccuracy(), $validation->getValidation(), $validation->getTraining()]);
        }

        $this->get('hepia.js_vars')->tData = $tData;
        $this->get('hepia.js_vars')->id = $id;

        $result = array('instance' => $instance, 'computers' => $computers, 'saves' => $saves);

        if (count($tData) > 0) {
            $result['max'] = max($tData);
        } else {
            $result['max'] = array(0);
        }

        return $this->render('hepiaThanatosBundle:Instance:view.html.twig', $result);
    }

    public function newAction(Request $request, $id) {
        $instance = new Instance();
        $computers = $this->container->get('hepia_thanatos.computer')->getAvailable();
        $formBuilder = $this->get('form.factory')->createBuilder(FormType::class, $instance);
        $formBuilder->add('title', TextType::class)
                ->add('save', SubmitType::class)
                ->add('network', EntityType::class, array(
                    'class' => 'hepiaThanatosBundle:Network',
                    'choice_label' => 'title',
                    'multiple' => false,
                ))
                ->add('data', EntityType::class, array(
                    'class' => 'hepiaThanatosBundle:Data',
                    'choice_label' => 'title',
                    'multiple' => false,))
                ->add('computers', ChoiceType::class, array('mapped' => false,
                    'choices' => $computers, 'multiple' => true));
        $form = $formBuilder->getForm();
        if ($request->isMethod('POST')) {
            $form->handleRequest($request);
            if ($form->isValid()) {
                $em = $this->getDoctrine()->getManager();
                $project = $em->getRepository('hepiaThanatosBundle:Project')->find($id);
                $instance->setProject($project);

                $i = 1;
                foreach ($form->get("computers")->getData() as $value) {
                    $new = clone $instance;
                    $new->setNumber($i);
                    $em->persist($new);
                    $em->flush();
                    $this->container->get('hepia_thanatos.computer')->launch($new->getId(), $value);
                    $i++;
                }
                return $this->redirectToRoute('hepia_thanatos_project_view', array('id' => $id));
            }
        }
        return $this->render('hepiaThanatosBundle:Instance:new.html.twig', array(
                    'form' => $form->createView(),
        ));
    }
}
