//
// Copyright (C) 2006,2007 Nicolas Rougier
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License as
// published by the Free Software Foundation; either version 2 of the
// License, or (at your option) any later version.
//
// $Id$

#ifndef __DANA_CORE_EVENT_H__
#define __DANA_CORE_EVENT_H__

#include <vector>
#include "object.h"


namespace dana { namespace core {

    typedef boost::shared_ptr<class Event> EventPtr;
    typedef boost::shared_ptr<class Observer> ObserverPtr;

    // ______________________________________________________________class Event
    class Event : public Object {

        // ___________________________________________________________attributes
    public:
        static std::vector<ObserverPtr>  observers;
        ObjectPtr                        subject;
        
    public:
        // _________________________________________________________________life
        Event (ObjectPtr subject = ObjectPtr());
        virtual ~Event (void);

        // _________________________________________________________________main
        static  void attach (ObserverPtr observer);
        static  void detach (ObserverPtr observer);
        virtual void notify (ObjectPtr subject);
        
        // _______________________________________________________________export
        static void python_export (void);
    };
}}

#endif