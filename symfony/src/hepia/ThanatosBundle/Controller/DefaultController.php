<?php

namespace hepia\ThanatosBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;
use Symfony\Bridge\Doctrine\Form\Type\EntityType;


class DefaultController extends Controller {

    public function indexAction() {

        $form = $this->createFormBuilder()
                ->setAction($this->generateUrl('hepia_thanatos_comparator'))
                ->add('instances', EntityType::class, array(
                    'class' => 'hepiaThanatosBundle:Instance',
                    'choice_label' => 'title',
                    'multiple' => true,))
                ->add('send', SubmitType::class)
                ->getForm();

        return $this->render('hepiaThanatosBundle:Default:index.html.twig', array('form' => $form->createView()));
    }

}
