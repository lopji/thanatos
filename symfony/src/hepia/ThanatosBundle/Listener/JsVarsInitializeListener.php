<?php

namespace hepia\ThanatosBundle\Listener;

class JsVarsInitializeListener {

    /**
     * @var \stdClass
     */
    private $jsVars;

    /**
     * @var boolean
     */
    private $appDebug;

    /**
     * @param \stdClass $jsVars
     * @param boolean $appDebug
     */
    public function __construct(\stdClass $jsVars, $appDebug) {
        $this->jsVars = $jsVars;
        $this->appDebug = $appDebug;
    }

    /**
     * Initialize js vars
     */
    public function onKernelController() {
        $this->jsVars->debug = $this->appDebug;
        $this->jsVars->websocket = array(
            'host' => '129.194.184.108',
            'port' => 8080,
        );
    }

}
